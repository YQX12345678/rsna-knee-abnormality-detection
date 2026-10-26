# Experiment Log

| Experiment | Effect | Conclusion |
|---|---:|---|
| DINOv2 6-slot baseline | - | start |
| + slot prior attention | +0.00x | small targets benefit |
| + TTA sliding window | +0.00x | slice redundancy used |
| + target-specific pooling | +0.00x | ACL/MCL top2, meniscus max, OA mean |
| DINOv3 5-fold | +0.00x | complementary to DINOv2 |
| Rad E13 inside Rad @0.50 | +0.00x | fat-sensitive planes + sagittal anchor |
| Rad E10 @0.50 | +0.00x | dual-branch fusion |
| E13 on E11 layout @0.15 | +0.00x | second pass, small but stable |
| Baker's / Fracture also Rad | -0.00x | Rad overfits on these two |
| U-Net 50% instead of 30% | -0.00x | blend weight matters more |

Open problem: Fracture and Contusion have very few samples, Macro AUC variance is high.
