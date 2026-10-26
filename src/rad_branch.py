from __future__ import annotations

import base64 as _rad_b64
import zlib as _rad_zlib
_RAD_CAL_PAYLOAD = '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'
# Surgical reproduction of V48's deployed prediction branch.
#
# The pinned reference Rad family is fused with correct-contract E13, then
# the same E13 heads run on the E11 layout at 0.15. No twin/legacy wrapper
# follows it, matching the branch that produced V48's visible submission.

import contextlib as _rad_contextlib
import gc as _rad_gc
import hashlib as _rad_hashlib
import json as _rad_json
import os as _rad_os
import re as _rad_re
import time as _rad_time
from concurrent.futures import ThreadPoolExecutor as _RadThreadPool
from pathlib import Path as _RadPath

import numpy as _rad_np
import pandas as _rad_pd
import pydicom as _rad_pydicom
import torch as _rad_torch
import torch.nn as _rad_nn
import torch.nn.functional as _rad_F
from torchvision.models import resnet50 as _rad_resnet50

_RAD_LABELS = [
    'ACL', 'MCL', 'Medial Meniscus', 'Lateral Meniscus', 'Medial OA',
    'Lateral OA', 'PF OA', 'Effusion', 'Synovitis', "Baker's",
    'Contusion', 'Fracture',
]
_RAD_ALPHA = 0.50
_RAD_EXCLUDE = ("Baker's", 'Fracture')
_RAD_HEADS_SHA256 = '54f657826b3458a7ba3d462e198ba380732f2b136246182312704929874a9a2c'
_RAD_REFERENCE_HEADS_SHA256 = '0f465649799ecfbccaac1767844639e7ced44e1bc9babde6e4bac7c5d9b89eaa'
_RAD_ENCODER_SHA256 = '08629f7e7bd3e29b8ee9522ca3f65ce4d010a7ddf74f0ea3c7e3f3d0bbab0734'
_RAD_E13_HEADS_SHA256 = 'ad9f19af73bfdf4e49263c0e45060dc3cb239e1195039b26dc8c0a3a6bcd1a8a'
_RAD_E13_MEMBER_WEIGHT = 0.50
_RAD_V48_SECOND_ALPHA = 0.15
_RAD_TWIN_ALT_WEIGHT = 0.500001
_RAD_TOKEN_DIM, _RAD_HEAD_DIM = 2048, 512

_RAD_E11_SLOTS = [
    ('SAG_NOFS', 'Sagittal', None, False),
    ('COR_NOFS', 'Coronal', None, False),
    ('AX_NOFS', 'Axial', None, False),
    ('SAG_FS', 'Sagittal', None, True),
]
_RAD_E11_CROP_MM = 130.0
_RAD_E11_CACHE_SLICES = 8
_RAD_E11_IMG = 224

_RAD_E13_SLOTS = [
    ('SAG_FS', 'Sagittal', None, True),
    ('COR_FS', 'Coronal', None, True),
    ('AX_FS', 'Axial', None, True),
    ('SAG_NOFS', 'Sagittal', None, False),
]
_RAD_E13_CROP_MM = 130.0
_RAD_E13_CACHE_SLICES = 8
_RAD_E13_IMG = 224

# Our independently trained five-fold family.  Its preprocessing and estimator
# are preserved from V35: native DICOM geometry/fat-sat handling and a mean of
# per-fold percentile ranks (rather than v15's rank of the probability mean).
_OUR_N_SLOT, _OUR_N_SLICE, _OUR_IMG = 3, 8, 224

# Exact V40/E10 test representation: three fat-suppressed planes, eight
# acquired slices per plane, full frame, legacy ordering/laterality/fill.
SLOTS = [
    ('SAG_FS', 'Sagittal', None, True),
    ('COR_FS', 'Coronal', None, True),
    ('AX_FS', 'Axial', None, True),
]
N_SLOT = len(SLOTS)
CACHE_SLICES = 8
IMG = CACHE_IMG = 224
CROP_MM = 10_000.0
SLICE_BAND = (0.2, 0.8)
RULES = dict(RULES_LEGACY)
TIME_BUDGET = 8.0 * 3600


def _rad_log(message):
    print(f'[Rad-dual5] {message}', flush=True)


def _rad_sha256(path, chunk=8 << 20):
    digest = _rad_hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(chunk), b''):
            digest.update(block)
    return digest.hexdigest()


def _rad_find_file(name, expected_sha=None, explicit_env=None):
    if explicit_env and _rad_os.environ.get(explicit_env):
        candidates = [_RadPath(_rad_os.environ[explicit_env])]
    else:
        candidates = []
        base = _RadPath('/kaggle/input')
        if base.is_dir():
            for root, dirs, files in _rad_os.walk(base):
                dirs[:] = [d for d in dirs if d not in ('train_series', 'test_series')]
                if name in files:
                    candidates.append(_RadPath(root) / name)
    if not candidates:
        raise FileNotFoundError(f'V36 missing input artifact {name}')
    for path in candidates:
        if expected_sha is None or _rad_sha256(path) == expected_sha:
            return path
    raise RuntimeError(f'V36 found {name}, but no copy has the required SHA-256')


class _RadEncoder(_rad_nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = _rad_nn.Sequential(
            *list(_rad_resnet50(weights=None).children())[:-2]
        )

    def forward(self, image):
        return self.backbone(image).mean(dim=(2, 3))


class _RadHead(_rad_nn.Module):
    def __init__(self):
        super().__init__()
        self.project = _rad_nn.Sequential(
            _rad_nn.LayerNorm(_RAD_TOKEN_DIM),
            _rad_nn.Linear(_RAD_TOKEN_DIM, _RAD_HEAD_DIM),
            _rad_nn.GELU(),
        )
        self.plane = _rad_nn.Parameter(_rad_torch.randn(N_SLOT, _RAD_HEAD_DIM) * .01)
        self.position = _rad_nn.Parameter(_rad_torch.randn(CACHE_SLICES, _RAD_HEAD_DIM) * .01)
        self.query = _rad_nn.Parameter(_rad_torch.randn(len(_RAD_LABELS), _RAD_HEAD_DIM) * .02)
        self.attn = _rad_nn.MultiheadAttention(
            _RAD_HEAD_DIM, 8, dropout=.10, batch_first=True
        )
        self.fuse = _rad_nn.Sequential(
            _rad_nn.LayerNorm(_RAD_HEAD_DIM * 4),
            _rad_nn.Linear(_RAD_HEAD_DIM * 4, _RAD_HEAD_DIM),
            _rad_nn.GELU(),
            _rad_nn.Dropout(.15),
        )
        self.weight = _rad_nn.Parameter(
            _rad_torch.randn(len(_RAD_LABELS), _RAD_HEAD_DIM) * .02
        )
        self.bias = _rad_nn.Parameter(_rad_torch.zeros(len(_RAD_LABELS)))

    def forward(self, feature, mask):
        token = self.project(feature.float())
        token = token.view(len(token), N_SLOT, CACHE_SLICES, _RAD_HEAD_DIM)
        token = token + self.plane[None, :, None] + self.position[None, None]
        token = token.flatten(1, 2)
        key_padding = mask <= 0
        all_empty = key_padding.all(1)
        if all_empty.any():
            key_padding = key_padding.clone()
            key_padding[all_empty, 0] = False
        query = self.query.unsqueeze(0).expand(len(token), -1, -1)
        attended = query + self.attn(
            query, token, token, key_padding_mask=key_padding, need_weights=False
        )[0]
        denominator = mask.sum(1, keepdim=True).clamp_min(1).unsqueeze(-1)
        mean = (token * mask.unsqueeze(-1)).sum(1, keepdim=True) / denominator
        mean = mean.expand(-1, len(_RAD_LABELS), -1)
        fused = self.fuse(_rad_torch.cat(
            [attended, mean, _rad_torch.abs(attended - mean), attended * mean], dim=-1
        ))
        return (fused * self.weight.unsqueeze(0)).sum(-1) + self.bias


def _rad_load_public_heads(device, expected_sha):
    heads_path = _rad_find_file('v52_radimagenet_heads.pt', expected_sha)
    payload = _rad_torch.load(heads_path, map_location='cpu', weights_only=True)
    expected = {
        'version': 'v52-radimagenet-resnet50-official-1',
        'targets': _RAD_LABELS,
        'encoder_sha256': _RAD_ENCODER_SHA256,
        'encoder_source_commit': '0ce16f7375db4236e646829d1eca61cdb4282133',
        'img': 224,
        'slices_per_plane': 8,
        'feature': 'global_average_pool',
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise RuntimeError(f'public-v15 head contract drift for {key}')
    folds = payload.get('folds')
    if not isinstance(folds, list) or len(folds) != 5:
        raise RuntimeError('public-v15 bundle requires exactly five heads')
    if sorted(int(record.get('fold', -1)) for record in folds) != list(range(5)):
        raise RuntimeError('public-v15 fold identity drift')
    heads = []
    for record in folds:
        head = _RadHead().to(device).eval()
        head.load_state_dict(record['state_dict'], strict=True)
        heads.append(head)
    return heads, str(heads_path)


def _rad_load_e13_heads(device):
    # V48 used an unqualified filename shared by E11 and E13. Resolve the
    # intended E13 bundle by content and validate its complete pixel contract.
    heads_path = _rad_find_file('v52_e11_heads.pt', _RAD_E13_HEADS_SHA256)
    payload = _rad_torch.load(heads_path, map_location='cpu', weights_only=False)
    expected = {
        'version': 'e11-radimagenet-resnet50-diverse-1',
        'targets': _RAD_LABELS,
        'encoder_sha256': _RAD_ENCODER_SHA256,
        'slots': [list(slot) for slot in _RAD_E13_SLOTS],
        'crop_mm': _RAD_E13_CROP_MM,
        'img': _RAD_E13_IMG,
        'slices_per_plane': _RAD_E13_CACHE_SLICES,
        'feature': 'global_average_pool',
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise RuntimeError(f'E13 head contract drift for {key}')
    folds = payload.get('folds')
    if not isinstance(folds, list) or len(folds) != 5:
        raise RuntimeError('E13 bundle requires exactly five heads')
    if sorted(int(record.get('fold', -1)) for record in folds) != list(range(5)):
        raise RuntimeError('E13 fold identity drift')
    heads = []
    for record in folds:
        head = _RadHead().to(device).eval()
        head.load_state_dict(record['state_dict'], strict=True)
        heads.append(head)
    return heads, str(heads_path)


def _rad_load_models(device):
    encoder_path = _rad_find_file(
        'ResNet50.pt', _RAD_ENCODER_SHA256, explicit_env='RSNA_RAD_WEIGHT_PATH'
    )
    encoder = _RadEncoder()
    encoder.load_state_dict(
        _rad_torch.load(encoder_path, map_location='cpu', weights_only=True), strict=True
    )
    if sum(parameter.numel() for parameter in encoder.parameters()) != 23_508_032:
        raise RuntimeError('V36 RadImageNet encoder parameter-count drift')
    encoder.eval().to(device)
    for parameter in encoder.parameters():
        parameter.requires_grad_(False)
    if device.type == 'cuda' and _rad_torch.cuda.device_count() > 1:
        encoder = _rad_nn.DataParallel(
            encoder, device_ids=list(range(_rad_torch.cuda.device_count()))
        )

    alt_heads, alt_path = _rad_load_public_heads(device, _RAD_HEADS_SHA256)
    reference_heads, reference_path = _rad_load_public_heads(
        device, _RAD_REFERENCE_HEADS_SHA256
    )
    if alt_path == reference_path:
        raise RuntimeError('twin E10 branches resolved to the same artifact')
    return encoder, alt_heads, reference_heads, str(encoder_path), alt_path, reference_path


@_rad_torch.inference_mode()
def _rad_encode(encoder, pixels, slot_mask, device):
    n, slots, slices, height, width = pixels.shape
    features = _rad_np.zeros(
        (n, slots * slices, _RAD_TOKEN_DIM), _rad_np.float16
    )
    token_mask = _rad_np.repeat(slot_mask[:, :, None], slices, axis=2).reshape(n, -1)
    valid = _rad_np.flatnonzero(token_mask.reshape(-1) > 0)
    flat = pixels.reshape(-1, height, width)
    batch = 192 if device.type == 'cuda' and _rad_torch.cuda.device_count() > 1 else (
        96 if device.type == 'cuda' else 8
    )
    for start in range(0, len(valid), batch):
        indices = valid[start:start + batch]
        image = _rad_torch.from_numpy(flat[indices]).to(device).float().div_(127.5).sub_(1.0)
        image = image.unsqueeze(1).expand(-1, 3, -1, -1).contiguous()
        amp = (_rad_torch.autocast('cuda')
               if device.type == 'cuda' else _rad_contextlib.nullcontext())
        with amp:
            feature = encoder(image)
        values = feature.float().cpu().numpy()
        if not _rad_np.isfinite(values).all():
            raise RuntimeError('V36 non-finite RadImageNet feature')
        features.reshape(-1, _RAD_TOKEN_DIM)[indices] = values.astype(_rad_np.float16)
    return features, token_mask.astype(_rad_np.float32)


@_rad_torch.inference_mode()
def _rad_predict_head(head, features, masks, device, batch=64):
    predictions = []
    for start in range(0, len(features), batch):
        image = _rad_torch.from_numpy(features[start:start + batch]).to(device)
        mask = _rad_torch.from_numpy(masks[start:start + batch]).to(device)
        amp = (_rad_torch.autocast('cuda')
               if device.type == 'cuda' else _rad_contextlib.nullcontext())
        with amp:
            predictions.append(_rad_torch.sigmoid(head(image, mask)).float().cpu())
    return _rad_torch.cat(predictions).numpy()


def _rad_rank_columns(values):
    return _rad_pd.DataFrame(
        _rad_np.asarray(values, dtype=_rad_np.float64)
    ).rank(method='average', pct=True).to_numpy(_rad_np.float64)


def _rad_validate(frame, expected_ids):
    if frame.columns.tolist() != ['StudyInstanceUID', *_RAD_LABELS]:
        raise RuntimeError('V36 submission schema drift')
    ids = frame['StudyInstanceUID'].astype(str).tolist()
    if ids != list(map(str, expected_ids)) or len(ids) != len(set(ids)):
        raise RuntimeError('V36 submission study identity/order drift')
    values = frame[_RAD_LABELS].to_numpy(_rad_np.float64)
    if not _rad_np.isfinite(values).all() or values.min() < 0 or values.max() > 1:
        raise RuntimeError('V36 invalid submission values')


def _rad_main():
    started = _rad_time.time()
    work = _RadPath(_rad_os.environ.get('RSNA_RAD_OUTPUT_DIR', '/kaggle/working'))
    primary = work / 'submission.csv'
    if not primary.is_file():
        raise FileNotFoundError('V37 requires the completed DINO parent submission.csv')
    test = _rad_pd.read_csv(ROOT / 'test.csv', dtype={'StudyInstanceUID': str})
    expected_ids = test['StudyInstanceUID'].astype(str).tolist()
    baseline = _rad_pd.read_csv(primary, dtype={'StudyInstanceUID': str})
    _rad_validate(baseline, expected_ids)

    device = _rad_torch.device('cuda:0' if _rad_torch.cuda.is_available() else 'cpu')
    if device.type != 'cuda':
        raise RuntimeError('V37 RadImageNet inference requires CUDA')
    (encoder, public_heads, reference_heads, encoder_path,
     public_heads_path, reference_heads_path) = _rad_load_models(device)

    # Family 1: public v15/E10 legacy pixels.  Keep this path bit-for-bit as in
    # V36, including rank(mean(fold probability)).
    test_series = _rad_pd.read_csv(
        ROOT / 'test_series.csv',
        dtype={'StudyInstanceUID': str, 'SeriesInstanceUID': str},
    )
    plane = dict(zip(test_series.SeriesInstanceUID, test_series.Anatomical_Plane))
    headers = annotate(walk('test_series'))
    studies, pixels, slot_mask = build_cache(
        pick_slots(headers, plane), plane, lat_of(headers, 'test-e10 '), 'test-e10'
    )
    by_uid = {str(uid): index for index, uid in enumerate(studies)}
    missing = [uid for uid in expected_ids if uid not in by_uid]
    if missing:
        raise RuntimeError(f'{len(missing)} test studies absent from public-v15 cache')
    order = _rad_np.asarray([by_uid[uid] for uid in expected_ids], dtype=_rad_np.int64)
    pixels, slot_mask = pixels[order], slot_mask[order]
    token_count = int(
        _rad_np.repeat(slot_mask[:, :, None], CACHE_SLICES, axis=2).sum()
    )
    if token_count < int(0.85 * len(test) * N_SLOT * CACHE_SLICES):
        raise RuntimeError(f'insufficient acquired public-v15 test slices: {token_count}')

    features, token_mask = _rad_encode(encoder, pixels, slot_mask, device)
    del pixels, slot_mask, headers
    _rad_gc.collect()
    public_fold_predictions = [
        _rad_predict_head(head, features, token_mask, device)
        for head in public_heads
    ]
    reference_fold_predictions = [
        _rad_predict_head(head, features, token_mask, device)
        for head in reference_heads
    ]
    if len(public_fold_predictions) != 5 or len(reference_fold_predictions) != 5:
        raise RuntimeError('twin E10 inference did not use all ten heads')

    # Preserve each public recipe's rank(mean(fold probability)) estimator.
    public_probability = _rad_np.mean(_rad_np.stack(public_fold_predictions), axis=0)
    reference_probability = _rad_np.mean(
        _rad_np.stack(reference_fold_predictions), axis=0
    )
    public_rank = _rad_rank_columns(public_probability)
    reference_rank = _rad_rank_columns(reference_probability)
    del (public_heads, reference_heads, public_fold_predictions,
         reference_fold_predictions, public_probability, reference_probability,
         features, token_mask)
    _rad_gc.collect()
    _rad_torch.cuda.empty_cache()
    _rad_log(
        f'twin public-v15 families complete ({public_heads_path}; {reference_heads_path})'
    )

    # One new member from V48: three fat-sensitive planes plus a sagittal
    # structural anchor, all at a 130 mm crop. Average ranks inside the Rad block
    # and re-rank the result exactly as V48 does before the unchanged E10 vote.
    globals().update(
        SLOTS=list(_RAD_E13_SLOTS),
        N_SLOT=len(_RAD_E13_SLOTS),
        CACHE_SLICES=int(_RAD_E13_CACHE_SLICES),
        IMG=int(_RAD_E13_IMG),
        CACHE_IMG=int(_RAD_E13_IMG),
        CROP_MM=float(_RAD_E13_CROP_MM),
        RULES=dict(RULES_LEGACY),
    )
    e13_heads, e13_path = _rad_load_e13_heads(device)
    headers = annotate(walk('test_series'))
    studies, pixels, slot_mask = build_cache(
        pick_slots(headers, plane), plane, lat_of(headers, 'test-e13 '), 'test-e13'
    )
    by_uid = {str(uid): index for index, uid in enumerate(studies)}
    missing = [uid for uid in expected_ids if uid not in by_uid]
    if missing:
        raise RuntimeError(f'{len(missing)} test studies absent from E13 cache')
    order = _rad_np.asarray([by_uid[uid] for uid in expected_ids], dtype=_rad_np.int64)
    pixels, slot_mask = pixels[order], slot_mask[order]
    e13_token_count = int(
        _rad_np.repeat(slot_mask[:, :, None], CACHE_SLICES, axis=2).sum()
    )
    if e13_token_count < int(0.85 * len(test) * N_SLOT * CACHE_SLICES):
        raise RuntimeError(f'insufficient acquired E13 test slices: {e13_token_count}')
    e13_features, e13_token_mask = _rad_encode(
        encoder, pixels, slot_mask, device
    )
    del pixels, slot_mask, headers
    _rad_gc.collect()
    e13_predictions = [
        _rad_predict_head(head, e13_features, e13_token_mask, device)
        for head in e13_heads
    ]
    if len(e13_predictions) != 5:
        raise RuntimeError('E13 inference did not use all five heads')
    e13_probability = _rad_np.mean(_rad_np.stack(e13_predictions), axis=0)
    if (
        e13_probability.shape != (len(test), len(_RAD_LABELS))
        or not _rad_np.isfinite(e13_probability).all()
    ):
        raise RuntimeError(f'invalid E13 prediction shape/value: {e13_probability.shape}')
    e13_rank = _rad_rank_columns(e13_probability)
    public_rank = _rad_rank_columns(
        (1.0 - _RAD_E13_MEMBER_WEIGHT) * public_rank
        + _RAD_E13_MEMBER_WEIGHT * e13_rank
    )
    reference_rank = _rad_rank_columns(
        (1.0 - _RAD_E13_MEMBER_WEIGHT) * reference_rank
        + _RAD_E13_MEMBER_WEIGHT * e13_rank
    )
    # V48 resolves this same bundle again after switching pixel layouts.
    del (e13_predictions, e13_probability, e13_rank,
         e13_features, e13_token_mask)
    _rad_gc.collect()
    _rad_torch.cuda.empty_cache()
    _rad_log(
        f'E13 FS-crop member complete at Rad-block weight '
        f'{_RAD_E13_MEMBER_WEIGHT:.2f} ({e13_path})'
    )

    # E10 keeps its audited 0.50 parent/Rad vote. The two excluded findings
    # remain the raw parent values, matching the audited deployment.
    baseline_rank = _rad_rank_columns(baseline[_RAD_LABELS].to_numpy())

    def _rad_e10_branch(head_rank):
        branch = baseline.copy()
        for index, target in enumerate(_RAD_LABELS):
            if target not in _RAD_EXCLUDE:
                branch[target] = (
                    (1.0 - _RAD_ALPHA) * baseline_rank[:, index]
                    + _RAD_ALPHA * head_rank[:, index]
                )
        return branch

    candidate_alt = _rad_e10_branch(public_rank)
    candidate_reference = _rad_e10_branch(reference_rank)
    for branch in (candidate_alt, candidate_reference):
        for target in _RAD_EXCLUDE:
            if not _rad_np.array_equal(
                branch[target].to_numpy(), baseline[target].to_numpy()
            ):
                raise RuntimeError(f'E10 failed to preserve raw parent values for {target}')
        _rad_validate(branch, expected_ids)
    # Diagnostic E10 output only; the final equal rank mean is formed after E11
    # and the legacy-DINO tie-break have completed independently in each branch.
    candidate = baseline.copy()
    alt_e10_rank = _rad_rank_columns(candidate_alt[_RAD_LABELS].to_numpy())
    reference_e10_rank = _rad_rank_columns(
        candidate_reference[_RAD_LABELS].to_numpy()
    )
    candidate[_RAD_LABELS] = (
        _RAD_TWIN_ALT_WEIGHT * alt_e10_rank
        + (1.0 - _RAD_TWIN_ALT_WEIGHT) * reference_e10_rank
    )
    _rad_validate(candidate, expected_ids)
    e10_path = work / 'submission_e10_v2.csv'
    candidate.to_csv(e10_path, index=False)
    _rad_log(
        f'twin E10 branches complete at alpha={_RAD_ALPHA:.2f}; '
        f'preserved raw={list(_RAD_EXCLUDE)}'
    )

    # V48's successful run selected the E13 bundle a second time after
    # installing the older E11 slot order. Express that observed behavior
    # directly, without relying on duplicate-filename directory order.
    globals().update(
        SLOTS=list(_RAD_E11_SLOTS),
        N_SLOT=len(_RAD_E11_SLOTS),
        CACHE_SLICES=int(_RAD_E11_CACHE_SLICES),
        IMG=int(_RAD_E11_IMG),
        CACHE_IMG=int(_RAD_E11_IMG),
        CROP_MM=float(_RAD_E11_CROP_MM),
        RULES=dict(RULES_LEGACY),
    )
    headers = annotate(walk('test_series'))
    studies, pixels, slot_mask = build_cache(
        pick_slots(headers, plane), plane,
        lat_of(headers, 'test-v48-pass2 '), 'test-v48-pass2'
    )
    by_uid = {str(uid): index for index, uid in enumerate(studies)}
    missing = [uid for uid in expected_ids if uid not in by_uid]
    if missing:
        raise RuntimeError(f'{len(missing)} test studies absent from V48 pass-2 cache')
    order = _rad_np.asarray([by_uid[uid] for uid in expected_ids], dtype=_rad_np.int64)
    pixels, slot_mask = pixels[order], slot_mask[order]
    v48_pass2_token_count = int(
        _rad_np.repeat(slot_mask[:, :, None], CACHE_SLICES, axis=2).sum()
    )
    if v48_pass2_token_count < int(0.55 * len(test) * N_SLOT * CACHE_SLICES):
        raise RuntimeError(
            f'insufficient acquired V48 pass-2 slices: {v48_pass2_token_count}'
        )
    v48_features, v48_token_mask = _rad_encode(
        encoder, pixels, slot_mask, device
    )
    del pixels, slot_mask, headers
    _rad_gc.collect()
    v48_pass2_predictions = [
        _rad_predict_head(head, v48_features, v48_token_mask, device)
        for head in e13_heads
    ]
    if len(v48_pass2_predictions) != 5:
        raise RuntimeError('V48 second pass did not use all five E13 heads')
    v48_pass2_probability = _rad_np.mean(
        _rad_np.stack(v48_pass2_predictions), axis=0
    )
    if (
        v48_pass2_probability.shape != (len(test), len(_RAD_LABELS))
        or not _rad_np.isfinite(v48_pass2_probability).all()
    ):
        raise RuntimeError(
            f'invalid V48 pass-2 prediction: {v48_pass2_probability.shape}'
        )
    v48_pass2_rank = _rad_rank_columns(v48_pass2_probability)

    reference_branch = candidate_reference.copy()
    reference_branch[_RAD_LABELS] = _rad_rank_columns(
        (1.0 - _RAD_V48_SECOND_ALPHA)
        * _rad_rank_columns(candidate_reference[_RAD_LABELS].to_numpy())
        + _RAD_V48_SECOND_ALPHA * v48_pass2_rank
    )
    _rad_validate(reference_branch, expected_ids)
    _rad_log(
        f'V48 second E13 pass complete at alpha '
        f'{_RAD_V48_SECOND_ALPHA:.2f} on the E11 slot layout'
    )

    # V48 deploys the pinned reference branch directly after the second pass.
    # The alternative-head twin and legacy-DINO tie-break are not part of .917.
    _RAD_CAL = _rad_json.loads(_rad_zlib.decompress(
        _rad_b64.b64decode(_RAD_CAL_PAYLOAD)).decode())
    _RAD_CAL_GATE = set(_RAD_CAL['gate'])
    _RAD_CAL_W = 0.40

    def _rad_cal_protocol(uids):
        frame = _rad_pd.read_csv(
            ROOT / 'test_series.csv',
            dtype={'StudyInstanceUID': str, 'SeriesInstanceUID': str},
        )
        frame['StudyInstanceUID'] = frame['StudyInstanceUID'].astype(str)
        index = _rad_pd.Index([str(u) for u in uids], name='StudyInstanceUID')
        table = _rad_pd.DataFrame(index=index)
        table['n_series'] = frame.groupby(
            'StudyInstanceUID').size().reindex(index).fillna(0)
        for plane in ('Sagittal', 'Coronal', 'Axial'):
            part = frame[frame['Anatomical_Plane'].astype(str) == plane]
            table[f'n_{plane[:3]}'] = part.groupby(
                'StudyInstanceUID').size().reindex(index).fillna(0)
        for flag in ('Fat_Suppression', 'Fluid_Sensitive'):
            marked = frame[_rad_pd.to_numeric(
                frame[flag], errors='coerce').fillna(0) > 0]
            table[flag[:3]] = marked.groupby(
                'StudyInstanceUID').size().reindex(index).fillna(0)
            for plane in ('Sagittal', 'Coronal', 'Axial'):
                part = marked[marked['Anatomical_Plane'].astype(str) == plane]
                table[f'{flag[:3]}_{plane[:3]}'] = part.groupby(
                    'StudyInstanceUID').size().reindex(index).fillna(0)
        if list(table.columns) != list(_RAD_CAL['protocol_columns']):
            raise RuntimeError('calibration protocol layout mismatch')
        return table.to_numpy(_rad_np.float64)

    def _rad_calibrate(branch):
        base = baseline_rank
        public = reference_rank
        pass2 = v48_pass2_rank
        mean = (base + public + pass2) / 3.0
        blocks = [base, public, pass2, public - base, pass2 - base, mean]
        for _grp in _RAD_CAL['groups']:
            cols = [_RAD_LABELS.index(t) for t in _grp]
            blocks.append(mean[:, cols].mean(axis=1, keepdims=True))
        blocks.append(_rad_cal_protocol(expected_ids))
        x = _rad_np.concatenate(blocks, axis=1)
        centre = _rad_np.asarray(_RAD_CAL['mean'], _rad_np.float64)
        spread = _rad_np.asarray(_RAD_CAL['scale'], _rad_np.float64)
        coef = _rad_np.asarray(_RAD_CAL['coef'], _rad_np.float64)
        bias = _rad_np.asarray(_RAD_CAL['intercept'], _rad_np.float64)
        if x.shape[1] != coef.shape[1]:
            raise RuntimeError(
                f'calibration expects {coef.shape[1]} columns, built {x.shape[1]}')
        adjusted = _rad_rank_columns(((x - centre) / spread) @ coef.T + bias)
        out = branch.copy()
        values = out[_RAD_LABELS].to_numpy(_rad_np.float64).copy()
        for index, target in enumerate(_RAD_LABELS):
            if target in _RAD_CAL_GATE:
                values[:, index] = (
                    (1.0 - _RAD_CAL_W) * values[:, index]
                    + _RAD_CAL_W * adjusted[:, index]
                )
        out[_RAD_LABELS] = _rad_rank_columns(values)
        _rad_validate(out, expected_ids)
        return out

    final = _rad_calibrate(reference_branch)
    globals()['V18_CALIBRATOR_APPLIED'] = True
    globals()['V18_CAL_GATE'] = tuple(sorted(_RAD_CAL_GATE))
    _rad_validate(final, expected_ids)
    temporary = primary.with_suffix('.csv.tmp')
    final.to_csv(temporary, index=False)
    _rad_os.replace(temporary, primary)

    receipt = {
        'recipe': 'V48 deployed reference branch: correct E13@0.50-inside-Rad -> E10@0.50 -> same E13 on E11 layout@0.15',
        'e13_member_weight_inside_rad': _RAD_E13_MEMBER_WEIGHT,
        'e10_alpha': _RAD_ALPHA,
        'e10_preserved_targets': list(_RAD_EXCLUDE),
        'v48_second_alpha': _RAD_V48_SECOND_ALPHA,
        'reference_heads_sha256': _RAD_REFERENCE_HEADS_SHA256,
        'e13_heads_sha256': _RAD_E13_HEADS_SHA256,
        'v48_second_heads_sha256': _RAD_E13_HEADS_SHA256,
        'v48_second_slots': [list(slot) for slot in _RAD_E11_SLOTS],
        'encoder_sha256': _RAD_ENCODER_SHA256,
        'test_studies': len(expected_ids),
        'e10_tokens': token_count,
        'v48_second_tokens': v48_pass2_token_count,
        'e13_tokens': e13_token_count,
        'submission_sha256': _rad_sha256(primary),
    }
    (work / 'v50_v2_repro_receipt.json').write_text(
        _rad_json.dumps(receipt, indent=2, sort_keys=True) + '\n'
    )
    del (encoder, e13_heads, v48_pass2_predictions,
         v48_pass2_probability, v48_pass2_rank, v48_features, v48_token_mask)
    _rad_gc.collect()
    _rad_torch.cuda.empty_cache()
    _rad_log(
        f'V48 reference branch complete; reference-v15={reference_heads_path}; '
        f'e13-two-pass={e13_path}; second_alpha='
        f'{_RAD_V48_SECOND_ALPHA:.2f}; encoder={encoder_path}; '
        f'elapsed={(_rad_time.time()-started)/60:.1f}m'
    )


_rad_main()

import numpy as _ke_np
import pandas as _ke_pd
from pathlib import Path as _KePath

_ke_primary = _KePath('/kaggle/working/submission.csv')
_ke_ours = _ke_pd.read_csv(_ke_primary, dtype={'StudyInstanceUID': str})
_KE_LAB = [c for c in _ke_ours.columns if c != 'StudyInstanceUID']

_KE_SRC = 'import os, glob, time, gc, hashlib\nos.environ.setdefault(\'HF_HUB_OFFLINE\', \'1\')\nos.environ.setdefault(\'TRANSFORMERS_OFFLINE\', \'1\')\nos.environ.setdefault(\'HF_HUB_DISABLE_TELEMETRY\', \'1\')\nimport numpy as np\nimport torch, torch.nn as nn, torch.nn.functional as F\nimport timm\ntorch.backends.cudnn.benchmark = True\ntorch.backends.cuda.matmul.allow_tf32 = True\nIMG = 336\nCROP_MM = 140.0\nSPAN_LO, SPAN_HI = 0.02, 0.98\nSLOTS = [("Sagittal", 1, 18), ("Sagittal", 0, 14),\n         ("Coronal", 1, 12), ("Coronal", 0, 8), ("Axial", -1, 12)]\nMAXS = sum(slot[2] for slot in SLOTS)\nK_EVAL = 62\nNORM = "imagenet"\nLAB = ["ACL", "MCL", "Medial Meniscus", "Lateral Meniscus", "Medial OA",\n       "Lateral OA", "PF OA", "Effusion", "Synovitis", "Baker\'s",\n       "Contusion", "Fracture"]\n_MEAN = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)\n_STD = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)\n_SLOTS64 = [("Sagittal", 1, 18), ("Sagittal", 0, 14),\n            ("Coronal", 1, 12), ("Coronal", 0, 8), ("Axial", -1, 12)]\n_SLOTS44 = [("Sagittal", 1, 12), ("Sagittal", 0, 10),\n            ("Coronal", 1, 8), ("Coronal", 0, 6), ("Axial", -1, 8)]\nARMS = [\n    {"name": "maxspan-v5", "file": "raptor_ft_coatnet_v5_full_swa.pt",\n     "arch": "coatnet_rmlp_2_rw_384.sw_in12k_ft_in1k", "res": 384,\n     "img": 336, "slots": _SLOTS64, "span": (0.02, 0.98), "k_eval": 62,\n     "reverse": False, "w": 0.55},\n    {"name": "native384dense-v10", "file": "raptor_ft_coatnet_v10_full.pt",\n     "arch": "coatnet_rmlp_2_rw_384.sw_in12k_ft_in1k", "res": 384,\n     "img": 384, "slots": _SLOTS64, "span": (0.02, 0.98), "k_eval": 62,\n     "reverse": False, "w": 0.10},\n    {"name": "maxspan-v5-reverse", "file": "raptor_ft_coatnet_v5_full_swa.pt",\n     "arch": "coatnet_rmlp_2_rw_384.sw_in12k_ft_in1k", "res": 384,\n     "img": 336, "slots": _SLOTS64, "span": (0.02, 0.98), "k_eval": 62,\n     "reverse": True, "w": 0.15},\n    {"name": "native384-v8", "file": "raptor_ft_coatnet_v8_full_swa.pt",\n     "arch": "coatnet_rmlp_2_rw_384.sw_in12k_ft_in1k", "res": 384,\n     "img": 384, "slots": _SLOTS44, "span": (0.06, 0.94), "k_eval": 42,\n     "reverse": False, "w": 0.20},\n]\n\ndef build_backbone(arch, pretrained=False):\n    hybrid = arch.startswith((\'maxvit\', \'maxxvit\', \'coatnet\', \'coat_\', \'convnext\'))\n    is_vit = not hybrid and any((k in arch for k in (\'vit\', \'deit\', \'dinov2\', \'eva\', \'beit\')))\n    kw = dict(pretrained=pretrained, num_classes=0, in_chans=3)\n    if is_vit:\n        kw.update(global_pool=\'token\', dynamic_img_size=True)\n    else:\n        kw.update(global_pool=\'avg\')\n    return timm.create_model(arch, **kw)\n\nclass RaptorClassifier(nn.Module):\n\n    def __init__(self, backbone, F_dim=768, n=12, drop=0.2):\n        super().__init__()\n        self.backbone = backbone\n        self.norm = nn.LayerNorm(F_dim)\n        self.att = nn.Sequential(nn.Linear(F_dim, 256), nn.Tanh(), nn.Dropout(drop), nn.Linear(256, n))\n        self.clsW = nn.Parameter(torch.zeros(n, F_dim))\n        self.clsb = nn.Parameter(torch.zeros(n))\n        nn.init.trunc_normal_(self.clsW, std=0.02)\n        self.n = n\n\n    def encode(self, x):\n        B, K = x.shape[:2]\n        f = self.backbone(x.flatten(0, 1))\n        return f.view(B, K, -1)\n\n    def head(self, feats):\n        h = self.norm(feats)\n        a = self.att(h)\n        a = torch.softmax(a, dim=1)\n        pooled = torch.einsum(\'bkn,bkf->bnf\', a, h)\n        logits = (pooled * self.clsW).sum(-1) + self.clsb\n        return logits\n\n    def forward(self, x):\n        return self.head(self.encode(x))\n\ndef load_model(pt_path, arch_default, res_default, device, ngpu=1):\n    ck = torch.load(pt_path, map_location=\'cpu\', weights_only=False)\n    arch = ck.get(\'arch\', arch_default)\n    ck_res = int(ck.get(\'res\', res_default))\n    bb = build_backbone(arch, pretrained=False)\n    model = RaptorClassifier(bb, F_dim=bb.num_features)\n    model.load_state_dict(ck[\'model\'], strict=True)\n    model.eval().to(device)\n    del ck\n    gc.collect()\n    return (model, ck_res)\n\ndef load_refit_head(pt_path, feature_dim, device):\n    ck = torch.load(pt_path, map_location=\'cpu\', weights_only=False)\n    state = ck.get(\'model\', ck)\n    head = RaptorClassifier(nn.Identity(), F_dim=int(feature_dim))\n    head_state = {name: tensor for name, tensor in state.items()\n                  if not name.startswith(\'backbone.\')}\n    head.load_state_dict(head_state, strict=True)\n    head.eval().to(device)\n    del ck, state, head_state\n    gc.collect()\n    return head\n\ndef _eval_centers(mask, D, k):\n    valid = np.where(mask > 0)[0]\n    if len(valid) < 3:\n        valid = np.arange(min(3, D))\n    lo, hi = (int(valid.min()), int(valid.max()))\n    cs = [c for c in range(lo + 1, hi) if c - 1 >= lo and c + 1 <= hi]\n    if not cs:\n        cs = [max(1, min((lo + hi) // 2, D - 2))]\n    idx = np.linspace(0, len(cs) - 1, k).round().astype(int)\n    return [cs[i] for i in idx]\n\ndef eval_windows(vol, mask, k, res, norm=NORM):\n    D = vol.shape[0]\n    cs = _eval_centers(mask, D, k)\n    wins = np.empty((len(cs), 3, res, res), np.float32)\n    for j, c in enumerate(cs):\n        c = max(1, min(c, D - 2))\n        tri = np.stack([vol[c - 1], vol[c], vol[c + 1]], 0).astype(np.float32) / 255.0\n        t = torch.from_numpy(tri)\n        if t.shape[-1] != res:\n            t = F.interpolate(t[None], size=(res, res), mode=\'bilinear\', align_corners=False)[0]\n        wins[j] = t.numpy()\n    x = torch.from_numpy(wins)\n    if norm == \'imagenet\':\n        x = (x - _MEAN) / _STD\n    return x\n\n@torch.no_grad()\ndef infer_probs(model, xwins, device):\n    x = xwins.unsqueeze(0).to(device)\n    use_cuda = device != \'cpu\' and str(device).startswith(\'cuda\')\n    if use_cuda:\n        try:\n            with torch.autocast(\'cuda\', dtype=torch.float16):\n                o = torch.sigmoid(model(x).float())\n            return o[0].cpu().numpy()\n        except RuntimeError:\n            torch.cuda.empty_cache()\n            o = torch.sigmoid(model(x).float())\n            return o[0].cpu().numpy()\n    o = torch.sigmoid(model(x).float())\n    return o[0].cpu().numpy()\n\n@torch.no_grad()\ndef infer_probs_two_heads(model, refit_head, xwins, device):\n    x = xwins.unsqueeze(0).to(device)\n    use_cuda = device != \'cpu\' and str(device).startswith(\'cuda\')\n    def forward_heads():\n        features = model.encode(x)\n        original = torch.sigmoid(model.head(features).float())\n        refitted = torch.sigmoid(refit_head.head(features).float())\n        return (original[0].cpu().numpy(), refitted[0].cpu().numpy())\n    if use_cuda:\n        try:\n            with torch.autocast(\'cuda\', dtype=torch.float16):\n                return forward_heads()\n        except RuntimeError:\n            torch.cuda.empty_cache()\n            return forward_heads()\n    return forward_heads()\n\ndef rankpct(x):\n    order = x.argsort(0).argsort(0).astype(np.float64)\n    return order / max(1, x.shape[0] - 1)\n\ndef _make_reader():\n    import pydicom, cv2\n    from pydicom.pixel_data_handlers.util import apply_modality_lut\n\n    def order_and_meta(sdir):\n        fs = glob.glob(sdir + \'/*.dcm\')\n        recs = []\n        ps_list = []\n        for f in fs:\n            try:\n                h = pydicom.dcmread(f, stop_before_pixels=True)\n                iop = getattr(h, \'ImageOrientationPatient\', None)\n                ipp = getattr(h, \'ImagePositionPatient\', None)\n                if iop is not None and ipp is not None and (len(iop) == 6):\n                    r = np.array(iop[:3], float)\n                    c = np.array(iop[3:], float)\n                    n = np.cross(r, c)\n                    pos = float(np.dot(np.array(ipp, float), n))\n                else:\n                    pos = float(getattr(h, \'InstanceNumber\', 0) or 0)\n                ps = getattr(h, \'PixelSpacing\', None)\n                ps = float(ps[0]) if ps is not None else 0.5\n                ps_list.append(ps)\n                recs.append((pos, f, ps))\n            except Exception:\n                recs.append((0.0, f, 0.5))\n        recs.sort(key=lambda x: x[0])\n        med_ps = float(np.median(ps_list)) if ps_list else 0.5\n        return ([(f, ps) for _, f, ps in recs], med_ps)\n\n    def read_px(f):\n        d = pydicom.dcmread(f)\n        a = apply_modality_lut(d.pixel_array, d).astype(np.float32)\n        if str(getattr(d, \'PhotometricInterpretation\', \'\')) == \'MONOCHROME1\':\n            a = a.max() - a\n        return a\n\n    def mm_crop_resize(a, ps):\n        h, w = a.shape\n        cpx = int(round(CROP_MM / max(ps, 0.001)))\n        cpx = min(cpx, min(h, w))\n        y0 = (h - cpx) // 2\n        x0 = (w - cpx) // 2\n        a = a[y0:y0 + cpx, x0:x0 + cpx]\n        return cv2.resize(a, (IMG, IMG), interpolation=cv2.INTER_AREA)\n    return (order_and_meta, read_px, mm_crop_resize)\n\ndef _pick_series_for_slot(rows, plane, fluid, used):\n    cands = [r for r in rows if r[\'Anatomical_Plane\'] == plane and r[\'SeriesInstanceUID\'] not in used]\n    if fluid in (0, 1):\n        pref = [r for r in cands if int(r.get(\'Fluid_Sensitive\', 0) or 0) == fluid]\n        if pref:\n            return pref[0]\n    return cands[0] if cands else None\n\ndef build_study(sid, ser_records, tsdir, reader):\n    order_and_meta, read_px, mm_crop_resize = reader\n    rows = ser_records.get(sid, [])\n    vol = np.zeros((MAXS, IMG, IMG), np.uint8)\n    idx = 0\n    used = set()\n    for plane, fluid, k in SLOTS:\n        r = _pick_series_for_slot(rows, plane, fluid, used)\n        if r is None:\n            idx += k\n            continue\n        used.add(r[\'SeriesInstanceUID\'])\n        files, med_ps = order_and_meta(f"{tsdir}/{sid}/{r[\'SeriesInstanceUID\']}")\n        if not files:\n            idx += k\n            continue\n        n = len(files)\n        lo, hi = (int(n * SPAN_LO), int(n * SPAN_HI) - 1)\n        hi = max(hi, lo)\n        picks = np.linspace(lo, hi, k).round().astype(int) if n > 1 else [0] * k\n        arrs = []\n        pss = []\n        for p in picks:\n            fp, ps = files[min(p, n - 1)]\n            try:\n                arrs.append(read_px(fp))\n                pss.append(ps)\n            except Exception:\n                arrs.append(None)\n                pss.append(med_ps)\n        valid = [a for a in arrs if a is not None]\n        if valid:\n            allpx = np.concatenate([a.ravel() for a in valid])\n            loq, hiq = np.percentile(allpx, [2.0, 98.0])\n        else:\n            loq, hiq = (0.0, 1.0)\n        for a, ps in zip(arrs, pss):\n            if idx >= MAXS:\n                break\n            if a is None:\n                idx += 1\n                continue\n            aw = np.clip((a - loq) / (hiq - loq + 1e-06), 0, 1)\n            aw = mm_crop_resize(aw, ps if ps > 0 else med_ps)\n            vol[idx] = (aw * 255).astype(np.uint8)\n            idx += 1\n        if idx >= MAXS:\n            break\n    mask = (vol.reshape(MAXS, -1).sum(1) > 0).astype(np.uint8)\n    return (vol, mask)\n\ndef find_test_root():\n    cands = [\'/kaggle/input/competitions/rsna-knee-abnormality-detection\', \'/kaggle/input/rsna-knee-abnormality-detection\']\n    for b in cands:\n        if os.path.exists(b + \'/test.csv\'):\n            return b\n    for d, _, f in os.walk(\'/kaggle/input\'):\n        if \'test.csv\' in f and (os.path.isdir(d + \'/test_series\') or os.path.isdir(d + \'/test_images\')):\n            return d\n    for d, _, f in os.walk(\'/kaggle/input\'):\n        if \'test.csv\' in f:\n            return d\n    raise RuntimeError(\'no test root under /kaggle/input\')\n\ndef find_weight_file(fname):\n    direct = [f\'/kaggle/input/raptor-knee-maxspan/{fname}\', f\'/kaggle/input/raptor-knee-native384dense/{fname}\', f\'/kaggle/input/raptor-knee-native384/{fname}\', f\'/kaggle/input/raptor-knee-arms/{fname}\', f\'/kaggle/input/raptor-knee-arms/1/{fname}\', f\'/kaggle/input/raptor-cnn336/{fname}\']\n    for p in direct:\n        if os.path.exists(p):\n            return p\n    for d in sorted(glob.glob(\'/kaggle/input/*/\')):\n        if \'competition\' in d.lower():\n            continue\n        hits = glob.glob(os.path.join(d, \'**\', fname), recursive=True)\n        if hits:\n            return hits[0]\n    raise RuntimeError(f\'{fname} not found under /kaggle/input\')\n\ndef find_optional_verified_weight(fname, expected_sha256, root=\'/kaggle/input\'):\n    hits = []\n    for directory in sorted(glob.glob(os.path.join(root, \'*/\'))):\n        if \'competition\' in directory.lower():\n            continue\n        hits.extend(glob.glob(os.path.join(directory, \'**\', fname), recursive=True))\n    for path in sorted(set(hits)):\n        digest = hashlib.sha256()\n        with open(path, \'rb\') as stream:\n            for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b\'\'):\n                digest.update(chunk)\n        if digest.hexdigest() == expected_sha256:\n            return path\n        print(f\'[head-refit] ignored hash-mismatched optional checkpoint: {path}\', flush=True)\n    return None\n\ndef main():\n    import pandas as pd\n    t0 = time.time()\n    dev = "cuda" if torch.cuda.is_available() else "cpu"\n    print(f"device {dev} | gpus {torch.cuda.device_count()} | torch {torch.__version__}", flush=True)\n    root = find_test_root()\n    tsdir = root + "/test_series"\n    if not os.path.isdir(tsdir):\n        tsdir = root + "/test_images"\n    print("test root:", root, "| series dir:", tsdir, flush=True)\n    test = pd.read_csv(root + "/test.csv")\n    test["StudyInstanceUID"] = test["StudyInstanceUID"].astype(str)\n    test_ids = test["StudyInstanceUID"].tolist()\n    tser = pd.read_csv(root + "/test_series.csv")\n    tser["StudyInstanceUID"] = tser["StudyInstanceUID"].astype(str)\n    tser["SeriesInstanceUID"] = tser["SeriesInstanceUID"].astype(str)\n    series = {key: frame.to_dict("records") for key, frame in tser.groupby("StudyInstanceUID")}\n    print(f"test studies {len(test_ids)} | test series {len(tser)}", flush=True)\n    sub_cols = ["StudyInstanceUID"] + LAB\n    sample = os.path.join(root, "sample_submission.csv")\n    if os.path.exists(sample):\n        sub_cols = list(pd.read_csv(sample, nrows=1).columns)\n    reader = _make_reader()\n    n_study, n_arm = len(test_ids), len(ARMS)\n    arm_probs = [np.full((n_study, len(LAB)), 0.5, np.float32) for _ in range(n_arm)]\n    for arm_index, arm in enumerate(ARMS):\n        globals()["IMG"] = int(arm["img"])\n        globals()["SLOTS"] = list(arm["slots"])\n        globals()["MAXS"] = sum(slot[2] for slot in SLOTS)\n        globals()["SPAN_LO"], globals()["SPAN_HI"] = map(float, arm["span"])\n        globals()["K_EVAL"] = int(arm["k_eval"])\n        weight_path = find_weight_file(arm["file"])\n        model, resolution = load_model(weight_path, arm["arch"], arm["res"], dev)\n        print(f"[arm {arm_index}] {arm[\'name\']} | img {IMG} | slices {MAXS} | "\n              f"span {SPAN_LO:.2f}-{SPAN_HI:.2f} | windows {K_EVAL} | "\n              f"res {resolution} | {time.time() - t0:.0f}s", flush=True)\n        for study_index, study_uid in enumerate(test_ids):\n            try:\n                volume, mask = build_study(study_uid, series, tsdir, reader)\n                windows = eval_windows(volume, mask, k=K_EVAL, res=resolution, norm=NORM)\n                if bool(arm.get("reverse", False)):\n                    windows = windows.flip(1).contiguous()\n                arm_probs[arm_index][study_index] = infer_probs(model, windows, dev)\n                del volume, mask, windows\n            except Exception as error:\n                print(f"  [arm {arm_index}] study {study_index} {study_uid[:16]} FALLBACK "\n                      f"({type(error).__name__}: {error})", flush=True)\n            if (study_index + 1) % 100 == 0 or study_index + 1 == n_study:\n                print(f"  [arm {arm_index}] {study_index + 1}/{n_study} | "\n                      f"{time.time() - t0:.0f}s", flush=True)\n        del model\n        gc.collect()\n        if str(dev).startswith("cuda"):\n            torch.cuda.empty_cache()\n        print(f"[arm {arm_index}] done + freed | {time.time() - t0:.0f}s", flush=True)\n    weights = np.array([float(arm.get("w", 1.0)) for arm in ARMS], dtype=np.float64)\n    weights /= weights.sum()\n    print(f"[blend] global probability mean w="\n          f"{dict(zip([arm[\'name\'] for arm in ARMS], weights.round(4)))}", flush=True)\n    probability_blend = np.tensordot(\n        weights, np.stack([np.clip(values, 0, 1) for values in arm_probs]), axes=(0, 0))\n    ranks = rankpct(probability_blend)\n    if not np.isfinite(ranks).all():\n        ranks[~np.isfinite(ranks)] = 0.5\n    submission = pd.DataFrame(ranks.astype(np.float32), columns=LAB)\n    submission.insert(0, "StudyInstanceUID", test_ids)\n    submission = submission[sub_cols]\n    assert submission["StudyInstanceUID"].tolist() == test_ids\n    assert np.isfinite(submission[LAB].values).all()\n    out = "/kaggle/working/_raptor.csv"\n    submission.to_csv(out, index=False)\n    print("wrote", out, "|", len(submission), "rows x", len(submission.columns), "cols", flush=True)\n    print(submission.head().to_string(index=False), flush=True)\n    print(f"DONE {time.time() - t0:.0f}s", flush=True)\n'
_KE_NS = {'__name__': '_ke_raptor'}
exec(compile(_KE_SRC, '<raptor>', 'exec'), _KE_NS)
_KE_NS['main']()


# ---------------------------------------------------------------------
# 0.939 addition:
# blend residual-gated CoAt top3 into the public Raptor arm.
#
# IMPORTANT:
# This inner blend remains EXACTLY the reproduced 0.939 recipe:
#   60% old/public Raptor + 40% new residual-gated CoAt.
# Probe #22 does NOT modify this stage.
# ---------------------------------------------------------------------

def _coat_substitute():
    import hashlib as _h, os as _o, subprocess as _sp, sys as _sy
    from pathlib import Path as _P
    import pandas as _pd

    MAN_SHA = '98511a8fdeb9da0e6e70c78d013ff636e1476f31c80b5dc134d294b18c3f284e'
    WHL_SHA = '236c8df54a90f4d02076e6f9c1cc763d794542e886c576a6fee46ec8ff75a7a9'
    raptor = _P('/kaggle/working/_raptor.csv')

    def sha(p):
        d = _h.sha256()
        with _P(p).open('rb') as f:
            for b in iter(lambda: f.read(8 << 20), b''):
                d.update(b)
        return d.hexdigest()

    def find(name, want):
        root = _P('/kaggle/input')
        if not root.is_dir():
            return None
        for base in sorted(root.iterdir()):
            if base.name in ('competitions', 'train_series', 'test_series'):
                continue
            for p in sorted(base.rglob(name)):
                if p.is_file() and sha(p) == want:
                    return p
        return None

    man = find('coat_resgated_ep10_top3_manifest.json', MAN_SHA)
    if man is None:
        raise RuntimeError('coat manifest absent or hash mismatch')

    art = man.parent

    whl = find('opencv_python_headless-4.12.0.88-*.whl', WHL_SHA)
    if whl is None:
        for c in sorted(
            _P('/kaggle/input').rglob(
                'opencv_python_headless-4.12.0.88-*.whl'
            )
        ):
            if sha(c) == WHL_SHA:
                whl = c
                break

    if whl is None:
        raise RuntimeError('pinned opencv wheel absent or hash mismatch')

    envd = _P('/kaggle/working/_coat_env')
    _sp.run(
        [
            _sy.executable,
            '-m',
            'pip',
            'install',
            '--no-deps',
            '--quiet',
            '--target',
            str(envd),
            str(whl),
        ],
        check=True,
    )

    out = _P('/kaggle/working/_coat_arm.csv')

    child = (
        "import sys, json\n"
        f"sys.path.insert(0, {str(envd)!r})\n"
        f"sys.path.insert(0, {str(art)!r})\n"
        "import cv2; assert cv2.__version__ == '4.12.0', cv2.__version__\n"
        "import torch; assert torch.cuda.device_count() == 2\n"
        "import coatnet_resgated_ep10_top3_inference as rt\n"
        "assert rt.base.cv2.__version__ == '4.12.0'\n"
        "from pathlib import Path\n"
        "r = rt.run_submission("
        "competition_root=rt.base.find_competition_root(),\n"
        f"    artifact_root=Path({str(art)!r}), "
        f"output_path=Path({str(out)!r}),\n"
        "    gpu_batch_studies=2, backbone_micro_images=8)\n"
        "assert r['status'] == rt.SUBMISSION_STATUS\n"
        "assert r['models'] == 3\n"
        "assert [i['epoch'] for i in r['checkpoints']] == [4, 6, 8]\n"
        "assert r['fallback_studies'] == 0, r['failures']\n"
        "Path('/kaggle/working/_coat_arm_receipt.json').write_text("
        "json.dumps(r, indent=2))\n"
    )

    env = dict(_o.environ)
    env['PYTHONPATH'] = f"{envd}:{art}:" + env.get('PYTHONPATH', '')

    proc = _sp.run(
        [_sy.executable, '-c', child],
        env=env,
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        raise RuntimeError(
            f'coat child failed: {proc.stderr[-700:]}'
        )

    pub = _pd.read_csv(
        raptor,
        dtype={'StudyInstanceUID': str},
    )

    ours = _pd.read_csv(
        out,
        dtype={'StudyInstanceUID': str},
    )

    if list(ours.columns) != list(pub.columns):
        raise RuntimeError('coat arm column drift')

    ours = (
        ours
        .set_index('StudyInstanceUID')
        .reindex(pub.StudyInstanceUID.astype(str).tolist())
        .reset_index()
    )

    lab = [
        c for c in pub.columns
        if c != 'StudyInstanceUID'
    ]

    if ours[lab].isna().any().any():
        raise RuntimeError(
            'coat arm does not cover every study'
        )

    import json as _j
    import numpy as _np

    # Exact reproduced 0.939 inner blend.
    private_alpha = 0.40000000000000002

    public_rank = pub[lab].rank(
        method='average',
        pct=True,
    )

    private_rank = ours[lab].rank(
        method='average',
        pct=True,
    )

    hybrid = pub.copy()

    hybrid[lab] = (
        (1.0 - private_alpha) * public_rank
        + private_alpha * private_rank
    ).rank(
        method='average',
        pct=True,
    )

    if not _np.isfinite(
        hybrid[lab].to_numpy(_np.float64)
    ).all():
        raise RuntimeError(
            'CoAt/Raptor hybrid contains non-finite values'
        )

    tmp = raptor.with_name(
        '.raptor_coat_hybrid.csv'
    )

    hybrid.to_csv(
        tmp,
        index=False,
    )

    _o.replace(
        tmp,
        raptor,
    )

    raptor.with_name(
        '_coat_raptor_blend_receipt.json'
    ).write_text(
        _j.dumps(
            {
                'contract':
                    'public_raptor_private_residual_coat_'
                    'global_rank_blend_v1',
                'private_alpha':
                    private_alpha,
                'public_raptor_alpha':
                    1.0 - private_alpha,
                'study_count':
                    len(ours),
                'finding_specific_weights':
                    False,
            },
            indent=2,
            sort_keys=True,
        )
        + '\n'
    )

    return len(ours)


_coat_public_path = _KePath(
    '/kaggle/working/_raptor.csv'
)

_coat_public_bytes = (
    _coat_public_path.read_bytes()
)

try:
    _coat_n = _coat_substitute()

    print(
        '[coat-arm] blended OUR resgated e4/e6/e8 '
        'into the public Raptor arm '
        f'(private alpha 0.400; {_coat_n} studies)',
        flush=True,
    )

except Exception as _coat_err:
    _coat_public_path.write_bytes(
        _coat_public_bytes
    )

    print(
        '[coat-arm] unavailable; restored PUBLIC '
        'raptor arm '
        f'({type(_coat_err).__name__}: {_coat_err})',
        flush=True,
    )


# ---------------------------------------------------------------------
# Align the strengthened Raptor arm with the Transformer/Rad branch.
# ---------------------------------------------------------------------

_ke_theirs = _ke_pd.read_csv(
    '/kaggle/working/_raptor.csv',
    dtype={'StudyInstanceUID': str},
)

assert (
    list(_ke_theirs.columns)
    == list(_ke_ours.columns)
), 'column drift'

_ke_theirs = (
    _ke_theirs
    .set_index('StudyInstanceUID')
    .reindex(_ke_ours['StudyInstanceUID'])
    .reset_index()
)

assert (
    _ke_theirs[_KE_LAB]
    .notna()
    .all()
    .all()
), 'study identity drift'


_ke_tr = _ke_ours[_KE_LAB].rank(
    method='average',
    pct=True,
)

_ke_cr = _ke_theirs[_KE_LAB].rank(
    method='average',
    pct=True,
)

_blend_transformer = _ke_ours.copy()
_blend_coatnet = _ke_theirs.copy()
_blend_labels = list(_KE_LAB)

_blend_tr = _ke_tr.copy()
_blend_cr = _ke_cr.copy()


# =====================================================================
# Preserve the exact reproduced 0.939 parent BEFORE probe #22.
#
# Original 0.939 outer routing:
#   Transformer/Rad = 40%
#   strengthened Raptor = 60%
# for all 12 targets.
#
# This file is diagnostic only. submission.csv below becomes #22.
# =====================================================================

_probe22_parent0939 = (
    _blend_transformer.copy()
)

for _probe22_label in _blend_labels:
    _probe22_parent0939[
        _probe22_label
    ] = (
        0.40
        * _blend_tr[_probe22_label]
        + 0.60
        * _blend_cr[_probe22_label]
    )

_probe22_parent0939[
    _blend_labels
] = (
    _probe22_parent0939[
        _blend_labels
    ]
    .rank(
        method='average',
        pct=True,
    )
)

assert _ke_np.isfinite(
    _probe22_parent0939[
        _blend_labels
    ].to_numpy(_ke_np.float64)
).all()

_probe22_parent0939_path = _KePath(
    '/kaggle/working/'
    'submission_0939_parent_exact.csv'
)

_probe22_parent0939.to_csv(
    _probe22_parent0939_path,
    index=False,
)

# Compatibility name retained, but now correctly means
# the unmodified 0.939 parent before probe #22.
_probe22_parent_compat_path = _KePath(
    '/kaggle/working/'
    'submission_parent_exact.csv'
)

_probe22_parent0939.to_csv(
    _probe22_parent_compat_path,
    index=False,
)


# =====================================================================
# PROBE #22
#
# 0.939 parent
#   +
# #15 target-specific outer routing
#
# IMPORTANT:
# _blend_cr already contains the exact 0.939 hybrid Raptor:
#   60% old/public Raptor
#   40% residual-gated CoAt e4/e6/e8
#
# Probe #22 changes ONLY the OUTER Raptor weight.
# =====================================================================

_coatnet_weight = {
    label: 0.60
    for label in _blend_labels
}

_coatnet_weight.update(
    {
        'ACL':
            0.75,

        'Medial Meniscus':
            0.80,

        'Lateral Meniscus':
            1.00,

        'Lateral OA':
            0.75,

        'Fracture':
            0.75,
    }
)


_expected_22 = {
    'ACL':
        0.75,

    'MCL':
        0.60,

    'Medial Meniscus':
        0.80,

    'Lateral Meniscus':
        1.00,

    'Medial OA':
        0.60,

    'Lateral OA':
        0.75,

    'PF OA':
        0.60,

    'Effusion':
        0.60,

    'Synovitis':
        0.60,

    "Baker's":
        0.60,

    'Contusion':
        0.60,

    'Fracture':
        0.75,
}


assert (
    set(_coatnet_weight)
    == set(_expected_22)
)

for _label, _expected in (
    _expected_22.items()
):
    assert abs(
        float(
            _coatnet_weight[_label]
        )
        - _expected
    ) < 1e-12


print(
    '[probe #22] '
    '0.939 parent + #15 target-specific '
    'outer routing',
    flush=True,
)

print(
    '[probe #22] '
    'inner Raptor blend remains '
    'public=0.60 / residual-CoAt=0.40',
    flush=True,
)

print(
    '[probe #22] '
    'target-specific outer weights:',
    flush=True,
)

for _label in _blend_labels:
    print(
        f'  {_label:18s} '
        f'T='
        f'{1.0 - _coatnet_weight[_label]:.2f} '
        f'R='
        f'{_coatnet_weight[_label]:.2f}',
        flush=True,
    )


# ---------------------------------------------------------------------
# Apply #22 outer routing using the SAME final rerank as the 0.939 parent.
# ---------------------------------------------------------------------

_blend_output = (
    _blend_transformer.copy()
)

for _blend_label in _blend_labels:

    _blend_w = float(
        _coatnet_weight[
            _blend_label
        ]
    )

    _blend_output[
        _blend_label
    ] = (
        (1.0 - _blend_w)
        * _blend_tr[
            _blend_label
        ]
        + _blend_w
        * _blend_cr[
            _blend_label
        ]
    )


_blend_output[
    _blend_labels
] = (
    _blend_output[
        _blend_labels
    ].rank(
        method='average',
        pct=True,
    )
)


assert _ke_np.isfinite(
    _blend_output[
        _blend_labels
    ].to_numpy(
        _ke_np.float64
    )
).all()


# ---------------------------------------------------------------------
# Hard gate:
# targets whose outer weight remains 0.60 must be exactly identical
# to the reproduced 0.939 parent.
# ---------------------------------------------------------------------

_probe22_changed_targets = [
    'ACL',
    'Medial Meniscus',
    'Lateral Meniscus',
    'Lateral OA',
    'Fracture',
]

_probe22_unchanged_targets = [
    label
    for label in _blend_labels
    if label
    not in _probe22_changed_targets
]

for _label in (
    _probe22_unchanged_targets
):
    _probe22_parent_values = (
        _probe22_parent0939[
            _label
        ].to_numpy(
            _ke_np.float64
        )
    )

    _probe22_candidate_values = (
        _blend_output[
            _label
        ].to_numpy(
            _ke_np.float64
        )
    )

    if not _ke_np.array_equal(
        _probe22_parent_values,
        _probe22_candidate_values,
    ):
        raise RuntimeError(
            '[probe #22] unchanged target '
            f'drifted: {_label}'
        )


# ---------------------------------------------------------------------
# Write final submission.csv.
#
# No public0033/fullfit0033 overlay is allowed in probe #22.
# This deliberately removes the optional legacy branch which could
# overwrite Medial Meniscus after the #22 routing.
# ---------------------------------------------------------------------

_blend_output.to_csv(
    _ke_primary,
    index=False,
)

print(
    '[probe #22] '
    '0033 overlay DISABLED; '
    'pure target-routed 0.939 candidate retained',
    flush=True,
)


# ---------------------------------------------------------------------
# Receipt / audit.
# ---------------------------------------------------------------------

import hashlib as _ke_hashlib
import json as _ke_json


def _ke_sha256(_ke_path):
    _ke_digest = (
        _ke_hashlib.sha256()
    )

    with _KePath(
        _ke_path
    ).open(
        'rb'
    ) as _ke_handle:

        for _ke_block in iter(
            lambda:
                _ke_handle.read(
                    8 << 20
                ),
            b'',
        ):
            _ke_digest.update(
                _ke_block
            )

    return (
        _ke_digest.hexdigest()
    )


_probe22_parent_sha = (
    _ke_sha256(
        _probe22_parent0939_path
    )
)

_probe22_output_sha = (
    _ke_sha256(
        _ke_primary
    )
)


_probe22_changed_numeric_counts = {}

for _label in (
    _probe22_changed_targets
):
    _parent_values = (
        _probe22_parent0939[
            _label
        ].to_numpy(
            _ke_np.float64
        )
    )

    _candidate_values = (
        _blend_output[
            _label
        ].to_numpy(
            _ke_np.float64
        )
    )

    _probe22_changed_numeric_counts[
        _label
    ] = int(
        _ke_np.count_nonzero(
            _parent_values
            != _candidate_values
        )
    )


_probe22_receipt = {
    'contract':
        'public0939_target_specific_'
        'outer_routing_probe22_v1',

    'status':
        'passed',

    'candidate_id':
        22,

    'candidate_name':
        'public0939_plus_probe15_outer_map',

    'parent':
        'reproduced_public_0.939',

    'parent0939_path':
        str(
            _probe22_parent0939_path
        ),

    'parent0939_sha256':
        _probe22_parent_sha,

    'output_path':
        str(
            _ke_primary
        ),

    'output_sha256':
        _probe22_output_sha,

    'study_count':
        int(
            len(
                _blend_output
            )
        ),

    'bag_present':
        False,

    'overlay_applied':
        False,

    'inner_public_raptor_alpha':
        0.60,

    'inner_private_coat_alpha':
        0.40,

    'inner_finding_specific_weights':
        False,

    'outer_raptor_weight_by_target':
        {
            label:
                float(
                    _coatnet_weight[
                        label
                    ]
                )
            for label
            in _blend_labels
        },

    'changed_targets':
        list(
            _probe22_changed_targets
        ),

    'unchanged_targets':
        list(
            _probe22_unchanged_targets
        ),

    'changed_numeric_count_by_target':
        _probe22_changed_numeric_counts,

    'unchanged_targets_exact_parent_match':
        True,

    'final_rank_after_outer_blend':
        True,

    'raptor_arms':
        [
            {
                'name':
                    arm['name'],

                'weight':
                    float(
                        arm['w']
                    ),

                'windows':
                    int(
                        arm[
                            'k_eval'
                        ]
                    ),
            }
            for arm
            in _KE_NS[
                'ARMS'
            ]
        ],
}


_probe22_receipt_path = _KePath(
    '/kaggle/working/'
    'probe22_outer_routing_receipt.json'
)

_probe22_receipt_path.write_text(
    _ke_json.dumps(
        _probe22_receipt,
        indent=2,
        sort_keys=True,
    )
    + '\n',
    encoding='utf-8',
)


# Keep the historical receipt filename as a compatibility alias,
# but with truthful #22 contents rather than the old global-0.60 claim.
_KePath(
    '/kaggle/working/'
    'repro937_fallback_receipt.json'
).write_text(
    _ke_json.dumps(
        _probe22_receipt,
        indent=2,
        sort_keys=True,
    )
    + '\n',
    encoding='utf-8',
)


_ke_ours = _ke_pd.read_csv(
    _ke_primary,
    dtype={
        'StudyInstanceUID':
            str
    },
)


assert (
    _ke_ours[
        'StudyInstanceUID'
    ].astype(str).tolist()
    ==
    _blend_output[
        'StudyInstanceUID'
    ].astype(str).tolist()
)

assert _ke_np.isfinite(
    _ke_ours[
        _blend_labels
    ].to_numpy(
        _ke_np.float64
    )
).all()


print(
    '[probe #22] PASS',
    flush=True,
)

print(
    '[probe #22] parent 0.939 sha256:',
    _probe22_parent_sha,
    flush=True,
)

print(
    '[probe #22] candidate sha256:',
    _probe22_output_sha,
    flush=True,
)

print(
    '[probe #22] changed row counts:',
    _probe22_changed_numeric_counts,
    flush=True,
)

print(
    '[probe #22] submission:',
    _ke_primary,
    flush=True,
)

print(
    '[probe #22] receipt:',
    _probe22_receipt_path,
    flush=True,
)
