# RSNA 2026 Knee MRI Abnormality Detection

**RSNA 2026 膝关节 MRI 多标签异常检测**：DINOv2/v3 多切片融合 + RadImageNet 双分支集成 + 目标级 rank 路由。

## 1. 竞赛背景

12 个目标：`ACL` `MCL` `Medial Meniscus` `Lateral Meniscus` `Medial OA` `Lateral OA` `PF OA` `Effusion` `Synovitis` `Baker's` `Contusion` `Fracture`。指标 Macro ROC-AUC。

## 2. 方案概览

- Stage 1 DINOv2 (HF)：6 slots x 3-slice windows，20 members，TTA + target pooling
- Stage 2 DINOv3 (timm)：ViT-Small，5-fold，slice-token + slot-token
- Stage 3 RadImageNet：ResNet-50 + label-query attention heads，dual branch
- Fusion：DINO parent + Rad branch -> target-level rank routing；Baker's / Fracture 保留父分支原值

## 3. 技术亮点

- **槽位先验注意力**：SlotHead 注入解剖先验，ACL 主要来自矢状面 FS/T1，PF OA 来自矢状+轴位。
- **TTA 目标级池化**：ACL/MCL top2，半月板 max，OA mean，Effusion/Synovitis mean。
- **权重指纹校验**：固定随机输入前向比对，tolerance 2e-3，防止预处理/架构漂移。
- **失败安全**：权重缺失保留 0.5 基准；单成员失败降权不中断；时间预算耗尽已完成成员出分。

## 4. 复现

    pip install -r requirements.txt
    export RSNA_DATA_ROOT=/path/to/rsna-knee-abnormality-detection
    bash scripts/download_weights.sh weights/
    python -m src.main --inference-only --data-root $RSNA_DATA_ROOT --weights weights/ --output submission.csv
    python -m src.main --data-root $RSNA_DATA_ROOT --weights weights/ --with-rad --parent-submission submission_round0.csv --output submission.csv

## 5. 结果

| Stage | Macro AUC |
|---|---:|
| DINOv2 20 members | 0.8xx |
| DINOv3 5-fold | 0.8xx |
| Rad dual-branch | 0.8xx |
| Final | **0.89+** |

## 6. 文件结构

    src/lexicon.py     报告结构化标签提取
    src/dataset.py     DICOM 槽位/排序/缓存
    src/model.py       SlotHead + DINOv2/v3 + 指纹校验
    src/rad_branch.py  RadImageNet 双分支
    src/ensemble.py    TTA + rank 集成
    src/main.py        CLI
    configs/default.yaml
    notebooks/rsna-knee-rentafork.ipynb
    docs/experiment_log.md
    docs/results.md
    scripts/download_weights.sh

## 7. 我的贡献

- 独立完成 DINOv2 骨干的槽位先验注意力设计与 TTA 窗口池化策略。
- 参与 RadImageNet 双分支的目标级 rank 路由调参，确定 Baker's / Fracture 保留父分支原值。
- 设计权重指纹校验与失败安全机制，保证 20 成员集成可复现。

**面试可展开**：槽位先验注意力动机、TTA 池化依据、Rad 分支为何排除 Baker's/Fracture、指纹校验如何防 drift。
