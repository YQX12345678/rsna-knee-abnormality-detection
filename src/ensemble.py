from __future__ import annotations

def take_group(cache_rows, g):
    return cache_rows[:, :, g * GROUP:(g + 1) * GROUP]

def augment(imgs, generator=None):
    lead = imgs.shape[:-3]
    x = imgs.reshape(-1, *imgs.shape[-3:]).float()
    n, dev = (x.shape[0], x.device)
    rot = (torch.rand(n, device=dev, generator=generator) - 0.5) * 2 * (AUG_ROT_DEG * np.pi / 180)
    sc = 1.0 + torch.rand(n, device=dev, generator=generator) * AUG_SCALE
    tx = (torch.rand(n, device=dev, generator=generator) - 0.5) * 2 * AUG_SHIFT
    ty = (torch.rand(n, device=dev, generator=generator) - 0.5) * 2 * AUG_SHIFT
    cos, sin = (torch.cos(rot) / sc, torch.sin(rot) / sc)
    theta = torch.zeros(n, 2, 3, device=dev, dtype=torch.float32)
    theta[:, 0, 0], theta[:, 0, 1], theta[:, 0, 2] = (cos, -sin, tx)
    theta[:, 1, 0], theta[:, 1, 1], theta[:, 1, 2] = (sin, cos, ty)
    grid = F.affine_grid(theta, x.shape, align_corners=False)
    x = F.grid_sample(x, grid, mode='bilinear', padding_mode='border', align_corners=False)
    scale = 1.0 + (torch.rand(n, 1, 1, 1, device=dev, generator=generator) - 0.5) * 2 * AUG_INTENSITY
    x = (x * scale).clamp(0, 255)
    return x.reshape(*lead, *x.shape[-3:]).to(imgs.dtype)

@torch.no_grad()
def predict(model, cache, mask, idx, dev, img_size=None):
    model.eval()
    out = []
    for b in range(0, len(idx), EVAL_BATCH):
        sel = idx[b:b + EVAL_BATCH]
        m = torch.from_numpy(mask[sel]).to(dev)
        acc = None
        for g in range(N_GROUP):
            rows = torch.from_numpy(np.ascontiguousarray(cache[sel, :, g * GROUP:(g + 1) * GROUP])).to(dev)
            with torch.autocast('cuda', enabled=dev.type == 'cuda'):
                z = model(rows, m, img_size).float()
            acc = z if acc is None else acc + z
        out.append(torch.sigmoid(acc / N_GROUP).cpu().numpy())
    return np.concatenate(out) if out else np.zeros((0, len(TARGETS)), np.float32)

def macro_auc(y, p):
    from sklearn.metrics import roc_auc_score
    return float(np.nanmean([roc_auc_score(y[:, j], p[:, j]) if len(set(y[:, j])) > 1 else np.nan for j in range(y.shape[1])]))

def write_submission(pred, studies, test_df, path):
    sub = pd.DataFrame(pd.DataFrame(pred).rank(pct=True).values, columns=TARGETS)
    sub.insert(0, 'StudyInstanceUID', studies)
    sub = test_df[['StudyInstanceUID']].merge(sub, on='StudyInstanceUID', how='left')
    sub[TARGETS] = sub[TARGETS].fillna(0.5)
    sub.to_csv(path, index=False)
    return sub

def write_benchmark_submission():
    t = pd.read_csv(ROOT / 'test.csv')
    for c in TARGETS:
        t[c] = 0.5
    t.to_csv('submission.csv', index=False)

def _v37_validate_submission(path, test_df, tag):
    path = Path(path)
    frame = pd.read_csv(path)
    expected = ['StudyInstanceUID'] + TARGETS
    if list(frame.columns) != expected:
        raise ValueError(f'{tag}: columns differ from the competition contract')
    if len(frame) != len(test_df) or not frame['StudyInstanceUID'].is_unique:
        raise ValueError(f'{tag}: row count or StudyInstanceUID uniqueness failed')
    if set(frame['StudyInstanceUID'].astype(str)) != set(test_df['StudyInstanceUID'].astype(str)):
        raise ValueError(f'{tag}: StudyInstanceUID set differs from test.csv')
    values = frame[TARGETS].to_numpy(np.float64)
    if not np.isfinite(values).all():
        raise ValueError(f'{tag}: non-finite prediction')
    return test_df[['StudyInstanceUID']].merge(frame, on='StudyInstanceUID', how='left')


def main():
    write_benchmark_submission()
    pkg = find_weights()
    if pkg is not None:
        dev = DEVS[0]
        infer_from_package(pkg, dev)
        try:
            test_df = pd.read_csv(ROOT / 'test.csv')
            native_path = Path('submission.csv')
            public_path = Path('submission_public_0899.csv')
            native = _v37_validate_submission(native_path, test_df, 'native 24-member')
            public = _v37_validate_submission(public_path, test_df, 'public DINO frontier')
            native.to_csv('submission_native_v38.csv', index=False)
            public.to_csv(native_path, index=False)
            promoted = _v37_validate_submission(native_path, test_df, 'V40 primary')
            if not promoted.equals(public):
                raise AssertionError('V40 serialization differs from validated public frontier')
            log('V40 primary = exact no-jitter public-frontier target pooling; native 24-member output retained')
        except Exception as public_frontier_error:
            log(f'public-frontier promotion skipped safely: {public_frontier_error}')
            traceback.print_exc()
        log('done')
        return
    read_labels(pd.read_csv(ROOT / 'train.csv', usecols=['StudyInstanceUID', 'Report']))
    test_df = pd.read_csv(ROOT / 'test.csv')
    test_series = pd.read_csv(ROOT / 'test_series.csv')
    train_df = pd.read_csv(ROOT / 'train.csv')
    train_series = pd.read_csv(ROOT / 'train_series.csv')
    log(f'train {train_df.shape} test {test_df.shape}')
    both = pd.concat([train_series, test_series])
    plane_map = dict(zip(both['SeriesInstanceUID'], both['Anatomical_Plane']))
    log('header pass: test')
    hte = annotate(walk('test_series'))
    log(f'  {len(hte)} test series')
    log('header pass: train')
    htr = annotate(walk('train_series'))
    log(f'  {len(htr)} train series')
    slots_te, slots_tr = (pick_slots(hte, plane_map), pick_slots(htr, plane_map))
    cov = pd.Series([len(v) for v in slots_tr.values()]).describe()
    log(f"train slots per study: mean {cov['mean']:.2f} min {cov['min']:.0f} max {cov['max']:.0f}")
    st_tr, Ctr, Mtr = build_cache(slots_tr, plane_map, lat_of(htr, 'train '), 'train')
    st_te, Cte, Mte = build_cache(slots_te, plane_map, lat_of(hte, 'test '), 'test')
    t_lab = time.time()
    lab = read_labels(train_df)
    log(f'derived labels for {len(lab)} studies in {time.time() - t_lab:.1f}s')
    gold = train_df.set_index('StudyInstanceUID')[TARGETS]
    gold = gold[gold.notna().all(axis=1)]
    Y = np.zeros((len(st_tr), len(TARGETS)), np.float32)
    W = np.zeros_like(Y)
    for i, st in enumerate(st_tr):
        if st in gold.index:
            Y[i], W[i] = (gold.loc[st].values, 3.0)
        elif st in lab.index:
            r = lab.loc[st]
            Y[i] = r[TARGETS].values
            W[i] = 0.25 + 0.75 * r[[t + '__conf' for t in TARGETS]].values
    keep = np.where(W.sum(1) > 0)[0]
    log(f'supervised {len(keep)} of {len(st_tr)} studies (annotated {len(gold)})')
    import hashlib
    rep = train_df.set_index('StudyInstanceUID')['Report'].fillna('')
    grp = np.array([int(hashlib.md5(rep.get(s, s).encode()).hexdigest()[:8], 16) % 5 for s in st_tr])
    va = np.array([i for i in keep if grp[i] == 0])
    tr = np.array([i for i in keep if grp[i] != 0])
    if len(va) == 0 or len(tr) < BATCH_STUDIES:
        cut = max(1, len(keep) // 5)
        va, tr = (keep[:cut], keep[cut:])
    log(f'train {len(tr)} / holdout {len(va)} studies')
    gpos = {s: i for i, s in enumerate(st_tr)}
    va_set = set(va.tolist())
    gi = np.array([gpos[s] for s in gold.index if s in gpos and gpos[s] in va_set])
    gold_y = gold.loc[[st_tr[i] for i in gi]].values.astype(int) if len(gi) else None
    yv = (Y[va] > 0.5).astype(int)
    log(f'annotation check: {len(gi)} of {len(gold)} annotated studies are in the holdout')
    dev = DEVS[0]
    results, test_preds = ({}, {})
    for cfg in RUNS:
        pitch = CROP_MM / cfg['img']
        log(f"=== {cfg['name']}: {cfg['img']} px, {pitch:.3f} mm/pixel, {pitch * 14:.2f} mm per patch token ===")
        torch.manual_seed(SEED)
        model = build_model(UNFREEZE_LAST).to(dev)
        opt = torch.optim.AdamW([{'params': [p for p in model.backbone.parameters() if p.requires_grad], 'lr': LR_BACKBONE}, {'params': model.head.parameters(), 'lr': LR_HEAD}], weight_decay=WEIGHT_DECAY)
        steps = max(EPOCHS * (len(tr) // BATCH_STUDIES), 1)
        sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=[LR_BACKBONE, LR_HEAD], total_steps=steps, pct_start=0.15)
        scaler = torch.amp.GradScaler('cuda', enabled=dev.type == 'cuda')
        best, best_state, best_annot = (-1.0, None, float('nan'))
        for ep in range(EPOCHS):
            model.train()
            perm = np.random.permutation(tr)
            tot, nstep = (0.0, 0)
            for b in range(0, len(perm) - BATCH_STUDIES + 1, BATCH_STUDIES):
                sel = perm[b:b + BATCH_STUDIES]
                rows = torch.from_numpy(Ctr[sel]).to(dev)
                g = int(torch.randint(N_GROUP, (1,)).item())
                imgs = augment(take_group(rows, g))
                m = torch.from_numpy(Mtr[sel]).to(dev)
                y = torch.from_numpy(Y[sel]).to(dev)
                w = torch.from_numpy(W[sel]).to(dev)
                with torch.autocast('cuda', enabled=dev.type == 'cuda'):
                    loss = (F.binary_cross_entropy_with_logits(model(imgs, m, cfg['img']), y, reduction='none') * w).mean()
                opt.zero_grad(set_to_none=True)
                scaler.scale(loss).backward()
                scaler.step(opt)
                scaler.update()
                sched.step()
                tot += loss.item()
                nstep += 1
            pv = predict(model, Ctr, Mtr, va, dev, cfg['img'])
            d = macro_auc(yv, pv)
            g_auc = float('nan')
            if gold_y is not None and len(gi):
                g_auc = macro_auc(gold_y, predict(model, Ctr, Mtr, gi, dev, cfg['img']))
            log(f'  epoch {ep + 1}/{EPOCHS}  loss {tot / max(nstep, 1):.4f}  holdout {d:.4f}  annot(n={len(gi)}) {g_auc:.4f}')
            if d > best:
                best, best_annot = (d, g_auc)
                best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            if time.time() - T0 > TIME_BUDGET:
                log('  time budget reached')
                break
        if best_state is not None:
            model.load_state_dict(best_state)
        results[cfg['name']] = (best, best_annot)
        test_preds[cfg['name']] = predict(model, Cte, Mte, np.arange(len(st_te)), dev, cfg['img'])
        log(f"  {cfg['name']}: best holdout {best:.4f} (annot {best_annot:.4f})")
        del model, opt, sched, scaler, best_state
        gc.collect()
        if dev.type == 'cuda':
            torch.cuda.empty_cache()
    log('---- summary ----')
    for n, (d, g_auc) in results.items():
        log(f'  {n:12s} holdout {d:.4f}   annot {g_auc:.4f}')
    pick = max(results, key=lambda k: results[k][0])
    log(f'best on the holdout: {pick} ({results[pick][0]:.4f})')
    for name, pred in test_preds.items():
        sub = write_submission(pred, st_te, test_df, f'submission_{name}.csv')
        log(f'  submission_{name}.csv {sub.shape}; nulls {int(sub[TARGETS].isna().sum().sum())}')
    ens = np.mean([pd.DataFrame(p).rank(pct=True).values for p in test_preds.values()], axis=0)
    write_submission(ens, st_te, test_df, 'submission_rankmean.csv')
    log(f'  submission_rankmean.csv (rank mean of {len(test_preds)})')
    sub = write_submission(test_preds[pick], st_te, test_df, 'submission.csv')
    log(f'submission.csv = {pick}; {sub.shape}; nulls {int(sub[TARGETS].isna().sum().sum())}')
    print(sub.head().to_string())

from scipy.stats import rankdata

def rank_ensemble(all_preds, weights=None):
    """排名集成：每个模型每个 target 独立排名后加权平均"""
    n_models = len(all_preds)
    if weights is None:
        weights = np.ones(n_models) / n_models
    n_studies, n_targets = all_preds[0].shape
    rank_sum = np.zeros((n_studies, n_targets))
    for i, pred in enumerate(all_preds):
        for j in range(n_targets):
            rank_sum[:, j] += weights[i] * rankdata(pred[:, j]) / n_studies
    final = np.zeros_like(rank_sum)
    for j in range(n_targets):
        final[:, j] = rankdata(rank_sum[:, j]) / n_studies
    return final

# ============================================================
# Cell 19: 主流程（仅推理，不做训练）
# 目的：快速验证 TTA 优化 + 集成权重调整的效果
# 预计耗时：2-3 分钟
# ============================================================

def main():
    # ============ 阶段 0: 保留原 0.900 推理 ============
    write_benchmark_submission()
    pkg = find_weights()
    if pkg is None:
        log('⚠️ 没找到权重包，无法推理')
        return

    dev = DEVS[0]
    try:
        infer_from_package(pkg, dev)
        # 保存推理结果
        test_df = pd.read_csv(ROOT / 'test.csv')
        submission_original = _v37_validate_submission('submission_round0.csv', test_df, 'original')
        submission_original.to_csv('submission_original.csv', index=False)
        submission_original.to_csv('submission.csv', index=False)   # ← 新增：把推理结果写回 submission.csv
        log(f'✅ 推理完成: submission.csv + submission_original.csv')
    except Exception as e:
        log(f'⚠️ 推理失败: {e}')
        traceback.print_exc()
        return

    # ============ 训练阶段全部跳过 ============
    log('=' * 60)
    log('跳过训练阶段（仅推理模式）')
    log('=' * 60)

    return submission_original


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        log('主流程失败，submission.csv 保留为 baseline')

_A5_SAVED = dict(globals())
import gc, os, time, warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import pydicom
import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
warnings.filterwarnings('ignore')
cv2.setNumThreads(1)
CROP_MM = 130.0
SIZE = 336
SLICE_BAND = (0.12, 0.88)
N_SLICE = 16
INTENSITY = 'slice'
SLOTS = [('Sagittal', 1), ('Sagittal', 0), ('Coronal', 1), ('Coronal', 0), ('Axial', 1), ('Axial', 0)]
N_SLOT = len(SLOTS)
LABELS = ['ACL', 'MCL', 'Medial Meniscus', 'Lateral Meniscus', 'Medial OA', 'Lateral OA', 'PF OA', 'Effusion', 'Synovitis', "Baker's", 'Contusion', 'Fracture']

def _find_dir(*names):
    root = Path('/kaggle/input')
    cand = []
    for n in names:
        cand += [root / n, root / 'competitions' / n, root / 'datasets' / n]
        for parent in (root / 'datasets', root / 'competitions', root):
            if parent.is_dir():
                try:
                    cand += [d / n for d in parent.iterdir() if d.is_dir()]
                except OSError:
                    pass
    for p in cand:
        if p.is_dir():
            return p
    return None
COMP = _find_dir('rsna-knee-abnormality-detection')
CKPT = _find_dir('knee-mri-fold-weights')
assert COMP is not None, 'competition data not attached'
assert CKPT is not None, 'fold weights not attached'
assert (COMP / 'sample_submission.csv').exists(), f'no competition data at {COMP}'
assert list(CKPT.glob('*_f*.pt')), f'no checkpoints at {CKPT}'
DEV = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'competition : {COMP}')
print(f'checkpoints : {CKPT}')
print(f'device      : {DEV}')
for i in range(torch.cuda.device_count() if DEV == 'cuda' else 0):
    cc = torch.cuda.get_device_capability(i)
    print(f'  gpu{i}       : {torch.cuda.get_device_name(i)} sm_{cc[0]}{cc[1]}, {torch.cuda.get_device_properties(i).total_memory / 2 ** 30:.0f} GiB, native bf16={cc >= (8, 0)}')

SERIES_ROOT = COMP / 'test_series'
if not SERIES_ROOT.exists():
    SERIES_ROOT = COMP / 'train_series'
print('series root:', SERIES_ROOT)

def ordered_files(sdir, cap=64):
    keyed = []
    for f in sdir.glob('*.dcm'):
        try:
            ds = pydicom.dcmread(str(f), stop_before_pixels=True)
            keyed.append((int(ds.InstanceNumber), str(f)))
        except Exception:
            continue
        if len(keyed) >= cap * 4:
            break
    return [f for _, f in sorted(keyed)]

def series_side(path):
    try:
        return float(pydicom.dcmread(path, stop_before_pixels=True).ImagePositionPatient[0])
    except Exception:
        return 0.0

def read_crop(path):
    try:
        ds = pydicom.dcmread(path)
        arr = ds.pixel_array.astype(np.float32)
    except Exception:
        return None
    try:
        ps = float(ds.PixelSpacing[0])
    except Exception:
        ps = CROP_MM / max(arr.shape)
    half = int(round(CROP_MM / ps / 2))
    cy, cx = (arr.shape[0] // 2, arr.shape[1] // 2)
    y0, y1 = (max(0, cy - half), min(arr.shape[0], cy + half))
    x0, x1 = (max(0, cx - half), min(arr.shape[1], cx + half))
    crop = arr[y0:y1, x0:x1]
    return None if crop.size == 0 else crop

def window(crop, lo, hi, flip):
    c = np.clip((crop - lo) / max(hi - lo, 1e-06), 0, 1)
    img = cv2.resize(c, (SIZE, SIZE), interpolation=cv2.INTER_AREA)
    return img[:, ::-1].copy() if flip else img

def render(path, flip):
    crop = read_crop(path)
    if crop is None:
        return None
    lo, hi = np.percentile(crop[::4, ::4], [1, 99])
    return window(crop, lo, hi, flip)

def build_study(args):
    idx, study, recs = args
    out = np.zeros((N_SLOT, N_SLICE, SIZE, SIZE), np.uint8)
    mask = np.zeros(N_SLOT, np.uint8)
    rows = pd.DataFrame(recs)
    if len(rows):
        for s_i, (plane, fs) in enumerate(SLOTS):
            sub = rows[(rows.Anatomical_Plane == plane) & (rows.Fat_Suppression == fs)]
            if sub.empty:
                continue
            files = ordered_files(SERIES_ROOT / study / sub.iloc[0].SeriesInstanceUID)
            if not files:
                continue
            flip = plane != 'Sagittal' and series_side(files[0]) < 0
            lo, hi = SLICE_BAND
            i0 = int(round(lo * (len(files) - 1)))
            i1 = int(round(hi * (len(files) - 1)))
            avail = list(range(i0, i1 + 1))
            if len(avail) >= N_SLICE:
                picks = [avail[int(round(t))] for t in np.linspace(0, len(avail) - 1, N_SLICE)]
                off = 0
            else:
                picks, off = (avail, (N_SLICE - len(avail)) // 2)
            if INTENSITY == 'series':
                crops = [read_crop(files[p]) for p in picks]
                got = [x for x in crops if x is not None]
                if got:
                    samp = np.concatenate([x[::4, ::4].ravel() for x in got])
                    lo_, hi_ = np.percentile(samp, [1, 99])
                    for c, x in enumerate(crops):
                        if x is None:
                            x = read_crop(files[min(len(files) - 1, picks[c] + 1)])
                        if x is not None:
                            out[s_i, off + c] = (window(x, lo_, hi_, flip) * 255).astype(np.uint8)
            else:
                for c, p in enumerate(picks):
                    img = render(files[p], flip)
                    if img is None:
                        img = render(files[min(len(files) - 1, p + 1)], flip)
                    if img is not None:
                        out[s_i, off + c] = (img * 255).astype(np.uint8)
            mask[s_i] = len(picks)
    return (idx, out, mask)
sub_df = pd.read_csv(COMP / 'sample_submission.csv')
ser_csv = pd.read_csv(COMP / 'test_series.csv')
if not (COMP / 'test_series').exists():
    ser_csv = pd.read_csv(COMP / 'train_series.csv')
ser_csv = ser_csv.loc[:, ~ser_csv.columns.duplicated()]
studies = sub_df.StudyInstanceUID.tolist()
by = {s: g.to_dict('records') for s, g in ser_csv[ser_csv.StudyInstanceUID.isin(set(studies))].groupby('StudyInstanceUID')}
print(f'{len(studies):,} test studies, {len(by):,} with series metadata')

N_SLOT_TYPES, MASK_IDX = (6, 0)

def segment_softmax(scores, sidx, B):
    T, K = scores.shape
    idx = sidx.unsqueeze(1).expand(-1, K)
    m = torch.full((B, K), float('-inf'), device=scores.device, dtype=scores.dtype)
    m = m.scatter_reduce(0, idx, scores, reduce='amax', include_self=True)
    e = (scores - m[sidx]).exp()
    s = torch.zeros(B, K, device=scores.device, dtype=scores.dtype).index_add_(0, sidx, e)
    return e / s[sidx].clamp(min=1e-06)

class MeanMaxPool(nn.Module):

    def forward(self, f, sidx, B, slot=None, return_attn=False):
        D = f.shape[1]
        cnt = torch.zeros(B, device=f.device, dtype=f.dtype).index_add_(0, sidx, torch.ones(f.shape[0], device=f.device, dtype=f.dtype))
        mean = torch.zeros(B, D, device=f.device, dtype=f.dtype).index_add_(0, sidx, f)
        mean = mean / cnt.clamp(min=1).unsqueeze(1)
        mx = torch.full((B, D), -10000.0, device=f.device, dtype=f.dtype)
        mx = mx.scatter_reduce(0, sidx.unsqueeze(1).expand(-1, D), f, reduce='amax', include_self=True)
        return (torch.cat([mean, mx], 1), None)

class LabelAttentionPool(nn.Module):

    def __init__(self, d, n_labels=12, n_heads=4, slot_bias=True):
        super().__init__()
        self.d, self.k, self.h = (d, n_labels, n_heads)
        self.q = nn.Parameter(torch.randn(n_labels, d) * 0.02)
        self.key, self.val = (nn.Linear(d, d), nn.Linear(d, d))
        self.slot_bias = nn.Parameter(torch.zeros(n_labels, N_SLOT_TYPES + 1)) if slot_bias else None

    def forward(self, f, sidx, B, slot=None, return_attn=False):
        scores = self.key(f) @ self.q.t() / self.d ** 0.5
        if self.slot_bias is not None and slot is not None:
            scores = scores + self.slot_bias.t()[slot]
        a = segment_softmax(scores, sidx, B)
        out = torch.zeros(B, self.k, self.d, device=f.device, dtype=f.dtype)
        out = out.index_add_(0, sidx, a.unsqueeze(-1) * self.val(f).unsqueeze(1))
        return (out, a)

class TokenXAttnPool(nn.Module):

    def __init__(self, d, n_labels=12, n_heads=6, dropout=0.2):
        super().__init__()
        self.d, self.k = (d, n_labels)
        self.q = nn.Parameter(torch.randn(n_labels, d) * 0.02)
        self.slot_emb = nn.Embedding(N_SLOT_TYPES + 1, d, padding_idx=0)
        self.kv_norm = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, n_heads, dropout=dropout, batch_first=True)

    def forward(self, tok, sidx, B, slot=None, return_attn=False):
        T, N, D = tok.shape
        cnt = torch.bincount(sidx, minlength=B)
        S = int(cnt.max().item())
        starts = torch.cumsum(cnt, 0) - cnt
        pos = torch.arange(T, device=tok.device) - starts[sidx]
        kv = tok + self.slot_emb(slot).unsqueeze(1)
        pad = tok.new_zeros(B, S, N, D)
        pad[sidx, pos] = kv
        keep = torch.zeros(B, S, dtype=torch.bool, device=tok.device)
        keep[sidx, pos] = True
        kpm = ~keep.repeat_interleave(N, dim=1)
        pad = self.kv_norm(pad.reshape(B, S * N, D))
        q = self.q.unsqueeze(0).expand(B, -1, -1)
        att, w = self.attn(q, pad, pad, key_padding_mask=kpm, need_weights=return_attn, average_attn_weights=True)
        cls = tok[:, 0]
        mean = torch.zeros(B, D, device=tok.device, dtype=tok.dtype).index_add_(0, sidx, cls) / cnt.clamp(min=1).unsqueeze(1)
        mx = torch.full((B, D), -10000.0, device=tok.device, dtype=tok.dtype)
        mx = mx.scatter_reduce(0, sidx.unsqueeze(1).expand(-1, D), cls, reduce='amax', include_self=True)
        base = torch.cat([mean, mx], 1).unsqueeze(1).expand(-1, self.k, -1)
        return (torch.cat([att, base], -1), w)

class ViTSlotToken(nn.Module):

    def __init__(self, vit, n_cat, dim=None):
        super().__init__()
        self.vit = vit
        d = dim or vit.embed_dim
        self.tok = nn.Embedding(n_cat + 1, d, padding_idx=MASK_IDX)
        self.num_features = vit.num_features
        self._orig_prefix = getattr(vit, 'num_prefix_tokens', 1)
        vit.num_prefix_tokens = self._orig_prefix + 1
        for blk in vit.blocks:
            a = getattr(blk, 'attn', None)
            if a is not None and hasattr(a, 'num_prefix_tokens'):
                a.num_prefix_tokens = a.num_prefix_tokens + 1

    @staticmethod
    def _maybe(mod, x):
        return x if mod is None else mod(x)

    def forward_features(self, x, cat):
        v = self.vit
        x = v.patch_embed(x)
        pos = v._pos_embed(x)
        rope = None
        if isinstance(pos, tuple):
            x, rope = pos
        else:
            x = pos
        x = self._maybe(getattr(v, 'patch_drop', None), x)
        x = self._maybe(getattr(v, 'norm_pre', None), x)
        npt = self._orig_prefix
        tok = self.tok(cat).unsqueeze(1)
        x = torch.cat([x[:, :npt], tok, x[:, npt:]], dim=1)
        if rope is not None:
            if getattr(v, 'rope_mixed', False):
                for i, blk in enumerate(v.blocks):
                    x = blk(x, rope=rope[i])
            else:
                for blk in v.blocks:
                    x = blk(x, rope=rope)
        else:
            x = v.blocks(x)
        return v.norm(x)

    def forward_head(self, x, pre_logits=True):
        return self.vit.forward_head(x, pre_logits=pre_logits)
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

class _GatedDepthBlock(nn.Module):

    def __init__(self, n_slice, dropout=0.0, ls_init=0.1):
        super().__init__()
        self.norm = nn.GroupNorm(1, n_slice)
        self.v = nn.Conv2d(n_slice, n_slice, 1)
        self.g = nn.Conv2d(n_slice, n_slice, 1)
        self.out = nn.Conv2d(n_slice, n_slice, 1)
        self.gamma = nn.Parameter(torch.full((n_slice, 1, 1), ls_init))
        self.drop = nn.Dropout2d(dropout) if dropout else nn.Identity()

    def forward(self, x):
        z = self.norm(x)
        return x + self.gamma * self.drop(self.out(self.v(z) * F.silu(self.g(z))))

class DepthCompress(nn.Module):

    def __init__(self, n_slice=16, out_ch=3, depth=1, dropout=0.0, ls_init=0.1, imagenet=True, proj_noise=0.25):
        super().__init__()
        self.imagenet = imagenet
        self.blocks = nn.ModuleList([_GatedDepthBlock(n_slice, dropout, ls_init) for _ in range(depth)])
        self.proj = nn.Conv2d(n_slice, out_ch, 1, bias=True)
        if imagenet:
            self.register_buffer('mu', torch.tensor(IMAGENET_MEAN).view(1, -1, 1, 1))
            self.register_buffer('sd', torch.tensor(IMAGENET_STD).view(1, -1, 1, 1))

    def forward(self, x):
        keep = (x.amax(dim=1, keepdim=True) > 0).to(x.dtype)
        z = x
        for b in self.blocks:
            z = b(z)
        z = self.proj(z)
        if self.imagenet:
            z = (z - self.mu.to(z.dtype)) / self.sd.to(z.dtype)
        return z * keep
N_PLANE, N_CONTRAST = (3, 2)
_PLANE_OF = lambda s: torch.clamp(s - 1, 0, 5) // 2
_CONTRAST_OF = lambda s: torch.clamp(s - 1, 0, 5) % 2

class SlotDepthMixer(nn.Module):

    def __init__(self, n_slice=16, ksize=5, alpha_max=0.25):
        super().__init__()
        self.n_slice, self.ksize, self.r = (n_slice, ksize, ksize // 2)
        self.alpha_max = alpha_max
        b = torch.tensor([1.0, 4.0, 6.0, 4.0, 1.0])
        self.register_buffer('base', b.log()[self.r:])
        n_u = self.r + 1
        self.shared = nn.Parameter(torch.zeros(n_u))
        self.plane_k = nn.Parameter(torch.zeros(N_PLANE, n_u))
        self.contrast_k = nn.Parameter(torch.zeros(N_CONTRAST, n_u))
        self.g0 = nn.Parameter(torch.zeros(()))
        self.gate_p = nn.Parameter(torch.zeros(N_PLANE))
        self.gate_c = nn.Parameter(torch.zeros(N_CONTRAST))
        idx = torch.arange(n_slice)
        self.register_buffer('off', idx[None, :] - idx[:, None])

    def kernel(self, slot):
        p, c = (_PLANE_OF(slot), _CONTRAST_OF(slot))
        half = self.base + self.shared + self.plane_k[p] + self.contrast_k[c]
        full = torch.cat([half.flip(-1)[..., :self.r], half], dim=-1)
        return F.softmax(full, dim=-1)

    def alpha(self, slot):
        p, c = (_PLANE_OF(slot), _CONTRAST_OF(slot))
        return self.alpha_max * torch.tanh(self.g0 + self.gate_p[p] + self.gate_c[c])

    def forward(self, x, slot, vmask):
        T, S, H, W = x.shape
        if vmask is None:
            raise ValueError('stem=mixer requires the padding mask')
        k = self.kernel(slot)
        v = vmask.to(k.dtype)
        d = self.off + self.r
        inb = (d >= 0) & (d < self.ksize)
        kk = k[:, d.clamp(0, self.ksize - 1)] * inb
        M = kk * v[:, None, :]
        den = M.sum(-1, keepdim=True)
        eye = torch.eye(S, device=x.device, dtype=M.dtype).expand(T, S, S)
        ok = (den > 1e-06) & v[:, :, None].bool()
        M = torch.where(ok, M / den.clamp(min=1e-06), eye)
        a = self.alpha(slot)[:, None, None]
        Aop = ((1.0 - a) * eye + a * M).to(x.dtype)
        if x.is_contiguous(memory_format=torch.channels_last) and (not x.is_contiguous()):
            y = torch.bmm(x.permute(0, 2, 3, 1).reshape(T, H * W, S), Aop.transpose(1, 2))
            return y.reshape(T, H, W, S).permute(0, 3, 1, 2)
        return torch.bmm(Aop, x.reshape(T, S, H * W)).reshape(T, S, H, W)

def _seg_mean_max(v, sidx, B):
    D = v.shape[1]
    cnt = torch.zeros(B, device=v.device, dtype=v.dtype).index_add_(0, sidx, torch.ones(v.shape[0], device=v.device, dtype=v.dtype))
    mean = torch.zeros(B, D, device=v.device, dtype=v.dtype).index_add_(0, sidx, v)
    mean = mean / cnt.clamp(min=1).unsqueeze(1)
    mx = torch.full((B, D), -10000.0, device=v.device, dtype=v.dtype)
    mx = mx.scatter_reduce(0, sidx.unsqueeze(1).expand(-1, D), v, reduce='amax', include_self=True)
    return torch.cat([mean, mx], 1)

def _pad_kv(x, sidx, B, norm):
    T, P, D = x.shape
    cnt = torch.bincount(sidx, minlength=B)
    S = int(cnt.max().item())
    starts = torch.cumsum(cnt, 0) - cnt
    pos = torch.arange(T, device=x.device) - starts[sidx]
    pad = x.new_zeros(B, S, P, D)
    pad[sidx, pos] = x
    keep = torch.zeros(B, S, dtype=torch.bool, device=x.device)
    keep[sidx, pos] = True
    return (norm(pad.reshape(B, S * P, D)), ~keep.repeat_interleave(P, dim=1))

class _GatedDelta(nn.Module):

    def __init__(self, d, n_labels, n_heads, dropout):
        super().__init__()
        self.q = nn.Parameter(torch.randn(n_labels, d) * 0.02)
        self.kv_norm = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, n_heads, dropout=dropout, batch_first=True)
        self.d_norm = nn.LayerNorm(d)
        self.dw = nn.Parameter(torch.randn(n_labels, d) * (1.0 / d ** 0.5))
        self.db = nn.Parameter(torch.zeros(n_labels))
        self.gate = nn.Parameter(torch.zeros(n_labels))

    def delta(self, pat, sidx, B, return_attn):
        kv, kpm = _pad_kv(pat, sidx, B, self.kv_norm)
        q = self.q.unsqueeze(0).expand(B, -1, -1)
        att, w = self.attn(q, kv, kv, key_padding_mask=kpm, need_weights=return_attn, average_attn_weights=True)
        return ((self.d_norm(att) * self.dw).sum(-1) + self.db, w)

class TokenResidualPool(_GatedDelta):

    def __init__(self, d, n_labels=12, n_heads=6, pe=64, dropout=0.2):
        super().__init__(d, n_labels, n_heads, dropout)
        self.base = nn.Sequential(nn.LayerNorm(2 * d + pe), nn.Dropout(dropout), nn.Linear(2 * d + pe, n_labels))

    def forward(self, tok, slot, sidx, B, pres, return_attn=False):
        base = self.base(torch.cat([_seg_mean_max(tok[:, 1:].mean(1), sidx, B), pres], 1))
        d_, w = self.delta(tok[:, 1:], sidx, B, return_attn)
        return (base + self.gate * d_, w)

class CodexResidualPool(_GatedDelta):

    def __init__(self, d, n_labels=12, n_heads=6, pe=64, dropout=0.2):
        super().__init__(d, n_labels, n_heads, dropout)
        self.base = nn.Sequential(nn.LayerNorm(2 * d + pe), nn.Dropout(dropout), nn.Linear(2 * d + pe, n_labels))

    def forward(self, tok, slot, sidx, B, pres, return_attn=False):
        base = self.base(torch.cat([_seg_mean_max(tok[:, 0], sidx, B), pres], 1))
        d_, w = self.delta(tok[:, 1:], sidx, B, return_attn)
        return (base + self.gate * d_, w)

class ClsAddPool(nn.Module):

    def __init__(self, d, n_labels=12, pe=64, dropout=0.2):
        super().__init__()
        self.net = nn.Sequential(nn.LayerNorm(4 * d + pe), nn.Dropout(dropout), nn.Linear(4 * d + pe, n_labels))

    def forward(self, tok, slot, sidx, B, pres, return_attn=False):
        return (self.net(torch.cat([_seg_mean_max(tok[:, 1:].mean(1), sidx, B), _seg_mean_max(tok[:, 0], sidx, B), pres], 1)), None)

class Readout(nn.Module):

    def __init__(self, pool, d, n_labels=12, pe=64):
        super().__init__()
        self.pool_kind, self.k = (pool, n_labels)
        self.pres_emb = nn.Embedding(N_SLOT_TYPES + 1, pe, padding_idx=0)
        if pool in ('xres', 'clsadd', 'xcodex'):
            self.pool = {'xres': TokenResidualPool, 'clsadd': ClsAddPool, 'xcodex': CodexResidualPool}[pool](d, n_labels, pe=pe)
        elif pool in ('attn', 'xattn'):
            if pool == 'xattn':
                self.pool = TokenXAttnPool(d, n_labels)
                wd = 3 * d + pe
            else:
                self.pool = LabelAttentionPool(d, n_labels)
                wd = d + pe
            self.norm = nn.LayerNorm(wd)
            self.w = nn.Parameter(torch.randn(n_labels, wd) * (1.0 / wd ** 0.5))
            self.b = nn.Parameter(torch.zeros(n_labels))
        else:
            self.pool = MeanMaxPool()
            self.net = nn.Sequential(nn.LayerNorm(2 * d + pe), nn.Dropout(0.2), nn.Linear(2 * d + pe, n_labels))
        self.drop = nn.Dropout(0.2)

    def forward(self, f, slot, sidx, B, return_attn=False):
        pe = self.pres_emb(slot)
        pres = torch.zeros(B, pe.shape[1], device=f.device, dtype=f.dtype).index_add_(0, sidx, pe)
        if self.pool_kind in ('xres', 'clsadd', 'xcodex'):
            return self.pool(f, slot, sidx, B, pres)[0]
        pooled, attn = self.pool(f, sidx, B, slot=slot, return_attn=return_attn)
        if self.pool_kind in ('attn', 'xattn'):
            x = torch.cat([pooled, pres.unsqueeze(1).expand(-1, self.k, -1)], -1)
            x = self.drop(self.norm(x))
            return (x * self.w).sum(-1) + self.b
        return self.net(torch.cat([pooled, pres], 1))

class Net(nn.Module):

    def __init__(self, enc, cond, n_meta=0, pool='mean_max', stem='native', n_slice=16):
        super().__init__()
        self.enc, self.cond = (enc, cond)
        self.compress = DepthCompress(n_slice, 3) if stem == 'compress' else None
        self.mixer = SlotDepthMixer(n_slice) if stem == 'mixer' else None
        self.tokens = pool in ('xattn', 'xres', 'clsadd', 'xcodex')
        D = enc.num_features
        self.meta_mlp = nn.Sequential(nn.LayerNorm(n_meta), nn.Linear(n_meta, 128), nn.GELU(), nn.Linear(128, D)) if n_meta > 0 else None
        self.readout = Readout(pool, D)
        if cond == 'post':
            self.slot_emb = nn.Embedding(N_SLOT_TYPES + 1, D, padding_idx=MASK_IDX)

    def forward(self, im, slot, smeta, sidx, B, vm=None):
        if self.mixer is not None:
            im = self.mixer(im, slot, vm)
        if self.compress is not None:
            im = self.compress(im)
        f = self.enc.forward_features(im, slot) if self.cond == 'token' else self.enc.forward_features(im)
        if self.tokens:
            inner = getattr(self.enc, 'vit', self.enc)
            orig = getattr(self.enc, '_orig_prefix', getattr(inner, 'num_prefix_tokens', 1))
            f = torch.cat([f[:, :1], f[:, orig:]], 1)
        else:
            f = self.enc.forward_head(f, pre_logits=True)
            if f.dim() > 2:
                f = f.flatten(1)
        ex = (lambda v: v.unsqueeze(1)) if self.tokens else lambda v: v
        if self.cond == 'post':
            f = f + ex(self.slot_emb(slot))
        if self.meta_mlp is not None and smeta.shape[1] > 0:
            mt = self.meta_mlp(smeta)
            f = torch.cat([f, mt.unsqueeze(1)], 1) if self.tokens else f + mt
        return self.readout(f, slot, sidx, B)
models = []
for ckpt_path in sorted(CKPT.glob('*_f*.pt')):
    z = torch.load(ckpt_path, map_location='cpu', weights_only=False)
    cfg = z['cfg']
    _stem = cfg.get('stem', 'native')
    _in = 3 if _stem == 'compress' else cfg.get('n_slice', 16)
    enc = timm.create_model(cfg['backbone'], pretrained=False, num_classes=0, in_chans=_in, **{'img_size': cfg['img']} if 'vit_' in cfg['backbone'] else {})
    if cfg['cond'] == 'token':
        enc = ViTSlotToken(enc, N_SLOT_TYPES)
    m = Net(enc, cfg['cond'], cfg.get('n_meta', 0), cfg['pool'], stem=_stem, n_slice=cfg.get('n_slice', 16))
    missing, unexpected = m.load_state_dict(z['state_dict'], strict=False)
    assert not [k for k in missing if not k.startswith('enc.')], f'missing {missing[:5]}'
    assert not unexpected, f'unexpected {unexpected[:5]}'
    models.append(m.eval())
    print(f"loaded {ckpt_path.name}  fold {z['fold']}  {cfg['backbone']} pool={cfg['pool']} meta={cfg['meta']}")
CFG = cfg
assert CFG.get('n_meta', 0) == 0, f"checkpoint expects {CFG['n_meta']} metadata features -- build slot_meta for the TEST studies and pass it to predict() before submitting"
print(f"\n{len(models)} fold models ready | input norm: {CFG.get('norm', 'none')}")

AMP_PREF = 'bf16'

def amp_for(dev):
    if not str(dev).startswith('cuda'):
        return (torch.float32, False)
    cc = torch.cuda.get_device_capability(dev)
    if AMP_PREF == 'bf16':
        return (torch.bfloat16, True)
    if AMP_PREF == 'fp16':
        return (torch.float16, True)
    if AMP_PREF == 'fp32':
        return (torch.float32, False)
    return (torch.bfloat16 if cc >= (8, 0) else torch.float16, True)
AMP_DT, AMP_ON = amp_for(DEV)
WORKERS = max(1, min(4, os.cpu_count() or 4))
CHUNK = 48
MICRO = 8
models = [m.to(DEV).eval() for m in models]
print(f"device {DEV} | amp {str(AMP_DT).split('.')[-1]} (on={AMP_ON}) | workers {WORKERS} | chunk {CHUNK} | micro {MICRO}")

def _norm_(im):
    k = CFG.get('norm', 'none')
    if k == 'zscore':
        m = (im > 0).float()
        n = m.sum(dim=(1, 2, 3), keepdim=True).clamp(min=1.0)
        mu = (im * m).sum(dim=(1, 2, 3), keepdim=True) / n
        var = (((im - mu) * m) ** 2).sum(dim=(1, 2, 3), keepdim=True) / n
        return (im - mu) / (var.sqrt() + 1e-06) * m
    if k == 'imagenet':
        m = (im > 0).float()
        return (im - 0.485) / 0.229 * m
    return im

@torch.no_grad()
def _micro(images, masks):
    dev = DEV
    ims, slots, sidx, vms = ([], [], [], [])
    for b in range(len(masks)):
        present = np.nonzero(masks[b] > 0)[0]
        if len(present) == 0:
            continue
        blk = images[b][present]
        ims.append(torch.from_numpy(blk))
        vms.append(torch.from_numpy(blk.reshape(blk.shape[0], blk.shape[1], -1).max(2) > 0))
        slots.append(torch.from_numpy(present + 1).long())
        sidx.append(torch.full((len(present),), b, dtype=torch.long))
    out = np.full((len(models), len(masks), len(LABELS)), np.nan, np.float32)
    if not ims:
        return out
    im = _norm_(torch.cat(ims).to(dev, non_blocking=True).float().div_(255.0))
    sl = torch.cat(slots).to(dev)
    si = torch.cat(sidx).to(dev)
    vm = torch.cat(vms).to(dev)
    sm = torch.zeros(len(sl), CFG.get('n_meta', 0), device=dev)
    per = torch.zeros(len(models), len(masks), len(LABELS), device=dev, dtype=torch.float32)
    with torch.autocast('cuda' if str(dev).startswith('cuda') else 'cpu', dtype=AMP_DT, enabled=AMP_ON):
        for fold_index, model in enumerate(models):
            per[fold_index] = torch.sigmoid(
                model(im, sl, sm, si, len(masks), vm=vm).float()
            )
    got = per.cpu().numpy()
    keep = np.array([(masks[b] > 0).any() for b in range(len(masks))])
    out[:, keep] = got[:, keep]
    return out

def predict(images, masks):
    out = np.full((len(models), len(masks), len(LABELS)), np.nan, np.float32)
    for a in range(0, len(masks), MICRO):
        b = min(a + MICRO, len(masks))
        out[:, a:b] = _micro(images[a:b], masks[a:b])
    return out

# Macro ROC-AUC depends on ordering, so combine fold orderings rather
# than allowing a fold's probability scale to dominate the mean.
preds = np.full((len(models), len(studies), len(LABELS)), np.nan, np.float32)
t0, done = (time.time(), 0)
with ProcessPoolExecutor(max_workers=WORKERS) as ex:
    for c0 in range(0, len(studies), CHUNK):
        block = studies[c0:c0 + CHUNK]
        imgs = np.zeros((len(block), N_SLOT, N_SLICE, SIZE, SIZE), np.uint8)
        msks = np.zeros((len(block), N_SLOT), np.uint8)
        futs = [ex.submit(build_study, (i, s, by.get(s, []))) for i, s in enumerate(block)]
        for f in as_completed(futs):
            try:
                i, a, k = f.result()
                imgs[i], msks[i] = (a, k)
            except Exception as e:
                print(f'  study failed: {type(e).__name__}: {e}')
        preds[:, c0:c0 + len(block)] = predict(imgs, msks)
        done += len(block)
        el = time.time() - t0
        print(f'  {done:,}/{len(studies):,}  {el / 60:.1f}m  eta {el / done * (len(studies) - done) / 60:.1f}m', flush=True)
        del imgs, msks
        gc.collect()
print(f'\ninference done in {(time.time() - t0) / 60:.1f} min')
A5_W = 0.45
A5_LABELS = list(LABELS)
_a5_ok = np.isfinite(preds).all(axis=(0, 2))
_a5_rank_mean = np.zeros((len(studies), len(LABELS)), np.float64)
for fold_index in range(preds.shape[0]):
    fold = preds[fold_index][_a5_ok]
    ordinal = fold.argsort(0).argsort(0).astype(np.float64)
    _a5_rank_mean[_a5_ok] += ordinal / max(len(fold) - 1, 1)
_a5_rank_mean /= preds.shape[0]
_a5_rank_mean[~_a5_ok] = np.nan
A5_PREDS = dict(zip(
    sub_df['StudyInstanceUID'].astype(str), _a5_rank_mean.astype(np.float32)
))
for _a5k, _a5v in _A5_SAVED.items():
    globals()[_a5k] = _a5v
del _A5_SAVED, _a5k, _a5v

_a5_sub = pd.read_csv('/kaggle/working/submission.csv',
                      dtype={'StudyInstanceUID': str})
assert _a5_sub.columns.tolist()[1:] == A5_LABELS, 'submission schema drift'
if A5_W > 0:
    _a5_ours = np.stack([A5_PREDS[_u]
                         for _u in _a5_sub['StudyInstanceUID'].astype(str)])
    _a5_base_rank = _a5_sub[A5_LABELS].rank(method='average', pct=True)
    _a5_ours_rank = pd.DataFrame(_a5_ours, columns=A5_LABELS,
                                 index=_a5_sub.index).rank(method='average', pct=True)
    _a5_sub[A5_LABELS] = (1.0 - A5_W) * _a5_base_rank + A5_W * _a5_ours_rank
    assert np.isfinite(_a5_sub[A5_LABELS].to_numpy()).all()
    _a5_sub.to_csv('/kaggle/working/submission.csv', index=False)
