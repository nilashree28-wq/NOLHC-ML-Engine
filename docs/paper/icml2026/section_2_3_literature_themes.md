# Section 2.3 — Literature Review Theme Paragraphs

**Source:** *Machine Learning and Simulation Frameworks for Border-Control Capacity Assessment: Evidence from Post-Brexit Agri-Food Logistics* (paper draft, Section 2.3)
**Transcribed from:** `Section_2.3_Five_Theme_Paragraphs (2).pdf`, shared for alignment check against [`uq_active_learning_loop_spec.md`](../../ml/spec/uq_active_learning_loop_spec.md)

Each paragraph introduces the concept, synthesises at least three studies comparatively, links the evidence to the present DES–ML framework (AnyLogic RoRo DES → NOLHC → multi-KPI surrogates → conformal UQ → UI screening), and cites sources for technical claims. Target length: 120–140 words per paragraph.

---

## Theme 1 — ML surrogates replacing expensive simulation in supply chains / logistics

Machine-learning surrogates treat expensive discrete-event simulation (DES) runs as labelled experiments and replace later full-system evaluations with fast predictors under limited budgets. Recent reviews show hybrid simulation–ML research in supply chains has intensified, using sequential and feedback data flows to overcome the separate limits of simulation and predictive modelling (Badakhshan, Mustafee and Bahadori, 2024; Kogler and Maxera, 2025). Relative to these broader taxonomies, Zhang et al. (2024) offer a more operational account: DES generates learning data under historical scarcity, and ML then runs alongside or instead of the simulator. Applied couplings likewise integrate regression or neural models with DES for cost and operational KPI estimation in maritime logistics (Le and Xuan-Thi-Thu, 2024). These findings motivate the present framework, where an AnyLogic RoRo border-control DES supplies training data for multi-KPI surrogates used in millisecond, human-on-the-loop screening.

## Theme 2 — LHS-designed experiments and comparing many surrogate families

When a metamodel replaces an expensive simulator, accuracy depends jointly on training-point placement and surrogate-family choice. Latin hypercube designs remain a standard space-filling strategy because they combine coverage with controllable factor correlation (Viana, 2016; Afzal, Kim and Seo, 2017). Later refinements, such as Latinised particle sampling, strengthen correlation control and information extraction from a single sample (Prots, Voigt and Mailach, 2023), while Afzal, Kim and Seo (2017) show that sample size and spatial distribution shape exploration–exploitation behaviour. On the modelling side, no family wins uniformly: the no-free-lunch principle requires problem-dependent selection rather than a universal default (Bogoclu, Roos and Nestorović, 2021). This joint design–model evidence underpins the present 129-run Nearly Orthogonal Latin Hypercube over border-control inputs and the per-KPI benchmark of multiple regressors.

## Theme 3 — Stacking and per-target ensemble selection

Stacking combines heterogeneous base learners through a meta-learner when fixing one inductive bias is risky for nonlinear simulator responses. Empirical studies report clear gains over single surrogates: optimised stacking cut cross-validated error sharply relative to base models in aquifer remediation (Shams, Alimohammadi and Yazdi, 2021), and local weighted stacking improved robustness in hydrodynamic prediction (Xu et al., 2022). Those gains are conditional. Hierarchical portfolio stacking and heterogeneous multiproblem surrogates retain ensembles only when generalisation error or adaptive validation justifies the complexity, and they filter candidates to avoid negative transfer (Ozelim et al., 2023; Li et al., 2025). Stacking is therefore best treated as a challenger to GPR or tree models, not an automatic upgrade. The present DES–ML engine follows that rule, registering Ridge stacking for a border-control KPI only when it improves cross-validated RMSE over the best individual surrogate.

## Theme 4 — Uncertainty: conformal prediction intervals and GPR variance

Point forecasts alone are insufficient for operational screening when DES outputs are stochastic and some KPIs approach congestion thresholds. Gaussian process regression provides useful predictive variance, yet those intervals can undercover under misspecification (Papadopoulos, 2023; Pion and Vazquez, 2024). Conformal prediction instead builds model-agnostic intervals with finite-sample marginal coverage that can wrap deterministic or probabilistic surrogates at low calibration cost (Gopakumar et al., 2024). Hybrid GP–conformal and hierarchical conformal methods further show that adaptive width and validity are complementary, and that GP or Bayesian calibration alone is often inadequate (Jaber et al., 2024; Shahbazi, Baheri and Azadeh-Fard, 2026). The shared prescription is to separate prediction from distribution-free uncertainty reporting. The present framework therefore attaches 90% split-conformal intervals to out-of-fold residuals of each selected KPI surrogate.

## Theme 5 — Closest end-to-end DES–ML analogues

End-to-end DES–ML analogues couple simulation, learning, and decision support rather than treating any layer alone. Supply-chain reviews document rapid growth in hybrid discrete simulation–machine learning research and identify sequential and feedback data-flow patterns linking the two methods (Kogler and Maxera, 2025; Badakhshan, Mustafee and Bahadori, 2024). Applied systems are more concrete but narrower: Zhang et al. (2024) use DES-generated data for predictive analytics under disruption, whereas Le and Xuan-Thi-Thu (2024) feed ML cost estimates into DES for sustainable maritime decisions. Relative to those hybrids, multi-KPI uncertainty reporting remains comparatively underdeveloped (Badakhshan, Mustafee and Bahadori, 2024). The present framework extends the shared sim→ML→decision-support logic by linking an AnyLogic border-control DES to NOLHC-trained multi-output surrogates and conformal intervals for offline, uncertainty-aware screening.

---

## Theme 6 — Native uncertainty from tree ensembles and ensemble disagreement

*(Task 1 SOTA review — extends Themes 1–5 with the same format; word count 138)*

Point predictions from Random Forest and Gradient Boosting carry no native variance, so the present framework currently borrows uncertainty from split-conformal residuals rather than the trees themselves. The infinitesimal jackknife recovers per-prediction variance from bootstrap covariance between trees, giving Random Forest a genuine standard error instead of one marginal band (Wager, Hastie and Efron, 2014). Quantile regression forests use each leaf's full conditional distribution to predict any quantile, not just the mean, while NGBoost reframes boosting as distributional regression via natural gradient parameters (Meinshausen, 2006; Duan et al., 2020). Deep and multi-output ensembles show that prediction spread across independently trained learners approximates epistemic uncertainty (Lakshminarayanan, Pritzel and Blundell, 2017; Yang and Yee, 2024). Applied here, these methods replace marginal per-KPI interval [conformal] with an input-dependent spread for each of the seven surrogates.

## Theme 7 — Batch/active learning for expensive simulators

*(word count 139)*

Sequential design turns experimentation into a loop: the surrogate flags where it is least reliable, the simulator is queried there, and the model retrains. Local hypercube refinement adds points where responses are non-uniform, correcting a fixed LHS design after the fact (Bogoclu, Roos and Nestorović, 2021). Batch-sequential design for stochastic simulators formalises replicating existing points versus exploring new ones, choosing whichever most reduces posterior predictive uncertainty under a fixed budget (Sürer, 2025). Active learning of deep-network surrogates shows the same logic scales to expensive physics simulators, with training-run selection outperforming uniform sampling under a limited query budget (Bajracharya et al., 2024). None of this touches a fixed, already-collected design: the 129-run NOLHC sample was drawn once and never revisited. A batch-sequential extension would spend new DES runs where the surrogate, not the original design, says they are needed.

## Theme 8 — Novelty/drift detection and separating DES noise from surrogate error

*(word count 140)*

A deployed surrogate faces inputs its training design never anticipated, and flagging a genuinely novel scenario is distinct from reporting interval width. Novelty-aware drift detection separates a shift from unfamiliar inputs from a shift in the input–output relationship (Shang, Zhang and Lu, 2025). CDSeer shows model-agnostic drift detection flags retraining need using a fraction of the labelled data earlier methods required, a real constraint given DES re-run cost (Pham et al., 2024). Stochastic kriging addresses a related problem, partitioning prediction uncertainty into intrinsic variance from stochastic replications and extrinsic variance from the metamodel, rather than one combined error term (Ankenman, Nelson and Staum, 2010). The present formulation, where a single epsilon absorbs both simulation noise and metamodel error, cannot make this distinction; separating the two decides whether an uncertain point needs another DES replication or a new design point.

---

## References cited in the theme paragraphs

Afzal, A., Kim, K. and Seo, J.-W. (2017) 'Effects of Latin hypercube sampling on surrogate modeling and optimization', *International Journal of Fluid Machinery and Systems*, 10, pp. 240–253. doi: 10.5293/ijfms.2017.10.3.240.

Badakhshan, E., Mustafee, N. and Bahadori, R. (2024) 'Application of simulation and machine learning in supply chain management: A synthesis of the literature using the Sim-ML literature classification framework', *Computers & Industrial Engineering*, 198, 110649. doi: 10.1016/j.cie.2024.110649.

Bogoclu, C., Roos, D. and Nestorović, T. (2021) 'Local Latin hypercube refinement for multi-objective design uncertainty optimization', *Applied Soft Computing*, 112, 107807. doi: 10.1016/j.asoc.2021.107807.

Gopakumar, V., Gray, A., Oskarsson, J., Zanisi, L., Pamela, S., Giles, D., Kusner, M.J. and Deisenroth, M. (2024) 'Uncertainty quantification of surrogate models using conformal prediction', *Machine Learning: Science and Technology*.

Jaber, E., Blot, V., Brunel, N., Chabridon, V., Remy, E., Iooss, B., Lucor, D., Mougeot, M. and Leite, A. (2024) 'Conformal approach to Gaussian process surrogate evaluation with coverage guarantees', arXiv preprint.

Kogler, C. and Maxera, P. (2025) 'A literature review of supply chain analyses integrating discrete simulation modelling and machine learning', *Journal of Simulation*, 20, pp. 110–134. doi: 10.1080/17477778.2025.2500393.

Le, L. and Xuan-Thi-Thu, T. (2024) 'Discovering supply chain operation towards sustainability using machine learning and DES techniques: a case study in Vietnam seafood', *Maritime Business Review*. doi: 10.1108/mabr-10-2023-0074.

Li, H., Xiong, P., Gong, M., Qin, A.K., Wu, Y. and Xing, L. (2025) 'Fast heterogeneous multiproblem surrogates for transfer evolutionary multiobjective optimization', *IEEE Transactions on Evolutionary Computation*.

Ozelim, L., Ribeiro, D., Schiavon, J.A., Domingues, V.R. and de Queiroz, P.I.B. (2023) 'HPOSS: A hierarchical portfolio optimization stacking strategy to reduce the generalization error of ensembles of models', *PLOS ONE*, 18. doi: 10.1371/journal.pone.0290331.

Papadopoulos, H. (2023) 'Guaranteed coverage prediction intervals with Gaussian process regression', *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 46, pp. 9072–9083. doi: 10.1109/tpami.2024.3418214.

Pion, A. and Vazquez, E. (2024) 'Gaussian process interpolation with conformal prediction: methods and comparative analysis', arXiv preprint.

Prots, A., Voigt, M. and Mailach, R. (2023) 'A charged particle-inspired sampling scheme for improved surrogate model quality', *Probabilistic Engineering Mechanics*. doi: 10.1016/j.probengmech.2023.103447.

Shahbazi, M.A., Baheri, A. and Azadeh-Fard, N. (2026) 'A hierarchical conformal framework for uncertainty-aware length of stay prediction in multi-hospital settings', *Scientific Reports*, 16. doi: 10.1038/s41598-026-37450-w.

Shams, R., Alimohammadi, S. and Yazdi, J. (2021) 'Optimized stacking, a new method for constructing ensemble surrogate models applied to DNAPL-contaminated aquifer remediation', *Journal of Contaminant Hydrology*, 243, 103914. doi: 10.1016/j.jconhyd.2021.103914.

Viana, F.A.C. (2016) 'A tutorial on Latin hypercube design of experiments', *Quality and Reliability Engineering International*, 32, pp. 1975–1985. doi: 10.1002/qre.1924.

Xu, G., Wei, H., Wang, J., Chen, X.-B. and Zhu, B. (2022) 'A local weighted linear regression (LWLR) ensemble of surrogate models based on stacking strategy: application to hydrodynamic response prediction for submerged floating tunnel (SFT)', *Applied Ocean Research*. doi: 10.1016/j.apor.2022.103228.

Zhang, T., Lauras, M., Zacharewicz, G., Rabah, S. and Bénaben, F. (2024) 'Coupling simulation and machine learning for predictive analytics in supply chain management', *International Journal of Production Research*, 62, pp. 8397–8414. doi: 10.1080/00207543.2024.2342019.

### References cited in Themes 6–8 (Task 1 SOTA additions, verified 23 Aug 2026)

Ankenman, B., Nelson, B.L. and Staum, J. (2010) 'Stochastic kriging for simulation metamodeling', *Operations Research*, 58(2), pp. 371–382. doi: 10.1287/opre.1090.0754.

Bajracharya, S. et al. (2024) 'Active learning of deep-network surrogates' — **citation unverified**; venue/DOI not confirmed by web search. Sakshi to supply full reference before this goes into the paper draft.

Bogoclu, C., Roos, D. and Nestorović, T. (2021) — see full reference above (Themes 1–5 list); reused here for the active-learning framing of local LHS refinement.

Duan, T., Anand, A., Ding, D.Y., Thai, K.K., Basu, S., Ng, A. and Schuler, A. (2020) 'NGBoost: Natural gradient boosting for probabilistic prediction', *Proceedings of the 37th International Conference on Machine Learning (ICML)*, PMLR 119, pp. 2690–2700.

Lakshminarayanan, B., Pritzel, A. and Blundell, C. (2017) 'Simple and scalable predictive uncertainty estimation using deep ensembles', *Advances in Neural Information Processing Systems*, 30, pp. 6402–6413. arXiv:1612.01474.

Meinshausen, N. (2006) 'Quantile regression forests', *Journal of Machine Learning Research*, 7, pp. 983–999.

Pham, T.M.T., Premkumar, K., Naili, M. and Yang, J. (2024) 'Time to retrain? Detecting concept drifts in machine learning systems' ["CDSeer"], arXiv:2410.09190.

Shang, D., Zhang, G. and Lu, J. (2025) 'Novelty-aware concept drift detection for neural networks', *Neurocomputing*, 617, 129012. doi: 10.1016/j.neucom.2024.129012.

Sürer, Ö. (2025) 'Batch sequential experimental design for calibration of stochastic simulation models', *Technometrics*. doi: 10.1080/00401706.2025.2520860. arXiv:2505.03990.

Wager, S., Hastie, T. and Efron, B. (2014) 'Confidence intervals for random forests: The jackknife and the infinitesimal jackknife', *Journal of Machine Learning Research*, 15, pp. 1625–1651.

Yang, X. and Yee, K. (2024) 'Towards reliable uncertainty quantification via deep ensemble in multi-output regression task', *Engineering Applications of Artificial Intelligence*, 132, 107871. doi: 10.1016/j.engappai.2024.107871.

---

## Alignment check against `uq_active_learning_loop_spec.md`

**No citation overlap** with the `docs/ManualScript/ML surrogates replacing simulation in supply chains.docx` scaffold — this is a distinct, more recent reference set (2016–2026, weighted toward 2023–2025) covering the same five themes with different sources. Nothing here contradicts the spec's current-state audit.

**Same five themes, same coverage boundary.** Both this document and the `ManualScript` scaffold stop at: sim→ML motivation, LHS/NOLHC design justification, stacking-as-challenger, and conformal + GPR-native UQ. Theme 4 here is in fact a stronger, more current version of the UQ theme already in the spec (Papadopoulos 2023, Pion & Vazquez 2024, Gopakumar et al. 2024, Jaber et al. 2024, Shahbazi et al. 2026 — all conformal/GPR, none tree-ensemble-native).

**Task 1 whitespace — status after Themes 6–8 (added by Sakshi, checked 23 Aug 2026).** Themes 6–8 above close most of the gap identified against Themes 1–5: Theme 6 covers RF jackknife/QRF/NGBoost + bootstrap/deep ensembles (spec §4.1 items 1–2), Theme 7 covers batch/active learning (item 4), Theme 8 covers novelty/drift detection + DES replication noise (items 5–6). All four of the riskier recent citations (Sürer 2025, Yang & Yee 2024, Shang/Zhang/Lu 2025, Pham et al. 2024/"CDSeer") were verified as real and correctly attributed via web search.

**Remaining open items:**
- Spec §4.1 item 3 (conformal-prediction extensions — jackknife+/CV+, Mondrian variants for heteroscedastic KPIs) has no dedicated paragraph; Theme 6 only cross-references conformal in passing. Optional 9th theme, or leave as scope call.
- Theme 6's claim "for each of the seven surrogates" does not match either registry in this repo (`nolhc_ml/models/v1/registry.json`: 4 tree-family winners; `experimenting_ml` SHAP-selected models: 5) — verify which snapshot the count of seven refers to before it's locked into the paper.
- Bajracharya et al. (2024) in Theme 7 is unverified — full reference (venue/DOI) still needed from Sakshi.
