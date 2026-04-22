import pandas as pd
from datetime import datetime, timedelta
import random

# 基于真实具身智能研究方向构造种子论文数据
papers_data = [
    {
        "title": "OpenVLA: An Open-Source Vision-Language-Action Model for Generalist Robot Manipulation",
        "summary": "We present OpenVLA, a 7B parameter open-source vision-language-action model pretrained on a diverse dataset of robot manipulation trajectories. OpenVLA achieves strong generalization across robot embodiments and tasks, outperforming prior closed-source models on benchmark evaluations. We release the model weights, training code, and evaluation suite.",
        "published": "2025-06-15",
        "authors": "Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, et al.",
        "link": "http://arxiv.org/abs/2506.00001",
        "primary_category": "cs.RO"
    },
    {
        "title": "π0: A Vision-Language-Action Flow Model for General Robot Control",
        "summary": "We introduce π0, a flow-based vision-language-action model trained on diverse robotic tasks spanning manipulation, mobility, and humanoid control. Our approach combines pretraining on internet-scale vision-language data with fine-tuning on robot-specific trajectories, achieving zero-shot generalization to novel tasks and environments.",
        "published": "2025-05-20",
        "authors": "Karl Pertsch, Kyle Stachowicz, Suraj Nair, et al.",
        "link": "http://arxiv.org/abs/2505.00002",
        "primary_category": "cs.RO"
    },
    {
        "title": "Dexterous Grasping with Tactile Sensing via Deep Reinforcement Learning",
        "summary": "This paper proposes a deep reinforcement learning framework for dexterous grasping that leverages high-resolution tactile sensing. Our method learns to interpret tactile feedback to adjust grasp strategies in real-time, achieving 94% success rate on previously unseen objects. We demonstrate results on a Shadow Hand robot platform.",
        "published": "2025-04-10",
        "authors": "Yijiong Lin, Jiaqi Jiang, et al.",
        "link": "http://arxiv.org/abs/2504.00003",
        "primary_category": "cs.RO"
    },
    {
        "title": "Humanoid Whole-Body Control via Model Predictive Control and Reinforcement Learning",
        "summary": "We present a hierarchical control framework for humanoid robots that combines model predictive control for trajectory optimization with reinforcement learning for policy adaptation. The approach enables robust locomotion over uneven terrain and dynamic manipulation tasks on a full-size humanoid platform.",
        "published": "2025-03-28",
        "authors": "Chen Yu, Zhang Wei, Li Ming, et al.",
        "link": "http://arxiv.org/abs/2503.00004",
        "primary_category": "cs.RO"
    },
    {
        "title": "Sim-to-Real Transfer for Contact-Rich Manipulation via Domain Randomization and Adaptation",
        "summary": "This work investigates sim-to-real transfer strategies for contact-rich manipulation tasks. We propose a combined approach of domain randomization during simulation training and online adaptation using real-world tactile feedback. Experiments demonstrate successful transfer from Isaac Sim to physical robot arms.",
        "published": "2025-02-15",
        "authors": "Alexander Li, Priya Sundaresan, et al.",
        "link": "http://arxiv.org/abs/2502.00005",
        "primary_category": "cs.RO"
    },
    {
        "title": "LeRobot: An Open-Source Framework for Robot Learning",
        "summary": "We introduce LeRobot, an open-source framework for robot learning that provides tools for dataset collection, model training, and policy evaluation. The framework includes pretrained models, simulated environments, and real-world robot interfaces. We demonstrate its effectiveness across multiple robot platforms and tasks.",
        "published": "2025-01-20",
        "authors": "Remi Cadene, Alexander Soane, et al.",
        "link": "http://arxiv.org/abs/2501.00006",
        "primary_category": "cs.AI"
    },
    {
        "title": "Neural Scene Representations for Embodied AI Navigation",
        "summary": "This paper explores neural scene representations for embodied navigation tasks. We propose a transformer-based architecture that processes visual observations to build implicit 3D scene representations, enabling efficient path planning and object search in novel environments.",
        "published": "2024-12-10",
        "authors": "Devendra Chaplot, Lisa Lee, et al.",
        "link": "http://arxiv.org/abs/2412.00007",
        "primary_category": "cs.CV"
    },
    {
        "title": "Multi-Modal Perception for Robot Manipulation: Fusing Vision, Tactile, and Proprioception",
        "summary": "We present a multi-modal perception framework that fuses visual, tactile, and proprioceptive sensing for robot manipulation. Our approach uses cross-attention mechanisms to integrate heterogeneous sensor streams, achieving robust perception under visual occlusion and contact uncertainty.",
        "published": "2024-11-05",
        "authors": "Roberto Calandra, Jingwei Xu, et al.",
        "link": "http://arxiv.org/abs/2411.00008",
        "primary_category": "cs.RO"
    },
    {
        "title": "Reinforcement Learning from Human Feedback for Robot Policy Fine-Tuning",
        "summary": "This work applies reinforcement learning from human feedback (RLHF) to fine-tune robot manipulation policies. We collect preference data from human operators comparing trajectory segments and train a reward model to align robot behavior with human intent. Results show significant improvement in task success and human satisfaction ratings.",
        "published": "2024-10-18",
        "authors": "Ajay Mandlekar, Danfei Xu, et al.",
        "link": "http://arxiv.org/abs/2410.00009",
        "primary_category": "cs.AI"
    },
    {
        "title": "Isaac Sim: A High-Performance Simulation Framework for Embodied AI Research",
        "summary": "We present Isaac Sim, a simulation framework built on NVIDIA Omniverse for embodied AI research. The framework provides photorealistic rendering, accurate physics simulation, and seamless sim-to-real transfer tools. We demonstrate its use for training policies that transfer to physical robots with minimal domain gap.",
        "published": "2024-09-22",
        "authors": "NVIDIA Research Team",
        "link": "http://arxiv.org/abs/2409.00010",
        "primary_category": "cs.RO"
    },
    {
        "title": "Language-Conditioned Imitation Learning for Generalizable Robot Skills",
        "summary": "We propose a language-conditioned imitation learning method that enables robots to acquire generalizable skills from human demonstrations paired with natural language instructions. Our approach uses a transformer-based policy architecture that jointly processes visual observations and language commands.",
        "published": "2024-08-14",
        "authors": "Corey Lynch, Pierre Sermanet, et al.",
        "link": "http://arxiv.org/abs/2408.00011",
        "primary_category": "cs.AI"
    },
    {
        "title": "Tactile Dexterity: Learning to Grasp with High-Resolution Touch Sensing",
        "summary": "This paper investigates the role of high-resolution tactile sensing in dexterous grasping. We develop a learning-based approach that processes raw tactile sensor arrays to predict grasp stability and adjust finger configurations. Results on a multi-fingered hand demonstrate improved grasp success compared to vision-only methods.",
        "published": "2024-07-30",
        "authors": "Wenzhen Yuan, Shaoxiong Wang, et al.",
        "link": "http://arxiv.org/abs/2407.00012",
        "primary_category": "cs.RO"
    },
    {
        "title": "Habitat 3.0: A Simulation Platform for Embodied AI with Humans",
        "summary": "We introduce Habitat 3.0, an extension of the Habitat simulation platform that enables embodied AI agents to interact with simulated human avatars. The platform supports multi-agent scenarios, social navigation tasks, and human-robot collaboration studies. We release benchmarks and pretrained models.",
        "published": "2024-06-12",
        "authors": "Meta AI Research Team",
        "link": "http://arxiv.org/abs/2406.00013",
        "primary_category": "cs.AI"
    },
    {
        "title": "End-to-End Visuomotor Policies for Precise Object Manipulation",
        "summary": "We present an end-to-end visuomotor policy architecture that directly maps raw pixel observations to motor commands for precise manipulation tasks. Our method combines convolutional visual encoding with recurrent state tracking, enabling sub-millimeter positioning accuracy without explicit state estimation.",
        "published": "2024-05-25",
        "authors": "Sergey Levine, Chelsea Finn, et al.",
        "link": "http://arxiv.org/abs/2405.00014",
        "primary_category": "cs.RO"
    },
    {
        "title": "Mobile Manipulation in Human-Centric Environments: Challenges and Solutions",
        "summary": "This survey paper examines the challenges of mobile manipulation in human-centric environments such as homes and offices. We categorize existing approaches by locomotion base, manipulation mechanism, and perception system, and identify key open problems including safety, semantic understanding, and long-horizon planning.",
        "published": "2024-04-08",
        "authors": "Oliver Kroemer, George Konidaris, et al.",
        "link": "http://arxiv.org/abs/2404.00015",
        "primary_category": "cs.RO"
    },
    {
        "title": "Transformer-Based Dynamics Models for Robot Learning",
        "summary": "We investigate the use of transformer architectures for learning robot dynamics models. Our approach models sequences of states and actions using self-attention, enabling accurate long-horizon prediction and efficient model-based reinforcement learning. Experiments demonstrate advantages over recurrent and feedforward baselines.",
        "published": "2024-03-15",
        "authors": "Michael Janner, Qiyang Li, et al.",
        "link": "http://arxiv.org/abs/2403.00016",
        "primary_category": "cs.LG"
    },
    {
        "title": "Few-Shot Adaptation of Vision-Language Models for Robot Instruction Following",
        "summary": "This paper proposes a few-shot adaptation method for applying large vision-language models to robot instruction following. Our approach leverages in-context learning and parameter-efficient fine-tuning to adapt pretrained models to novel robot embodiments and task domains with minimal demonstration data.",
        "published": "2024-02-20",
        "authors": "Dhruv Batra, Roozbeh Mottaghi, et al.",
        "link": "http://arxiv.org/abs/2402.00017",
        "primary_category": "cs.CV"
    },
    {
        "title": "Safe Reinforcement Learning for Physical Human-Robot Interaction",
        "summary": "We develop safe reinforcement learning methods for physical human-robot interaction scenarios. Our approach incorporates safety constraints derived from human biomechanics and uses constrained optimization to ensure collision forces remain below safe thresholds during close-proximity collaboration tasks.",
        "published": "2024-01-10",
        "authors": "Andrea Bajcsy, Dylan Losey, et al.",
        "link": "http://arxiv.org/abs/2401.00018",
        "primary_category": "cs.RO"
    },
    {
        "title": "Foundation Models for Robotics: Opportunities and Challenges",
        "summary": "This position paper discusses the application of foundation models to robotics. We analyze how large language models and vision-language models can provide prior knowledge for robot learning, examine current limitations including embodiment mismatch and action grounding, and outline a research agenda for developing robot-specific foundation models.",
        "published": "2023-12-05",
        "authors": "Yuke Zhu, Jitendra Malik, et al.",
        "link": "http://arxiv.org/abs/2312.00019",
        "primary_category": "cs.AI"
    },
    {
        "title": "Diffusion Policies as an Expressive Policy Class for Offline Reinforcement Learning",
        "summary": "We introduce diffusion policies, a new policy representation for offline reinforcement learning based on diffusion models. Our approach models the distribution of actions conditioned on observations, enabling multimodal behavior and improved performance on complex manipulation tasks compared to Gaussian policy parameterizations.",
        "published": "2023-11-18",
        "authors": "Cheng Chi, Siyuan Feng, et al.",
        "link": "http://arxiv.org/abs/2311.00020",
        "primary_category": "cs.LG"
    },
    {
        "title": "Learning Bipedal Locomotion via Adversarial Motion Priors",
        "summary": "We propose a method for learning bipedal locomotion skills by combining adversarial motion priors with reinforcement learning. Our approach extracts motion priors from human gait data and uses adversarial training to encourage natural walking patterns. Results on a humanoid robot demonstrate robust locomotion across various terrains.",
        "published": "2023-10-22",
        "authors": "Xue Bin Peng, Michiel van de Panne, et al.",
        "link": "http://arxiv.org/abs/2310.00021",
        "primary_category": "cs.RO"
    },
    {
        "title": "Semantic Affordance Grasping: Learning to Grasp Objects by Function",
        "summary": "This work introduces semantic affordance grasping, where robots learn to grasp objects according to their intended function rather than just geometric stability. We construct a large-scale dataset of functional grasps and train a model that predicts grasp poses conditioned on task descriptions, achieving higher task success rates than geometry-only methods.",
        "published": "2023-09-14",
        "authors": "Trevor Darrell, Jitendra Malik, et al.",
        "link": "http://arxiv.org/abs/2309.00022",
        "primary_category": "cs.CV"
    },
    {
        "title": "Continual Learning for Long-Term Autonomy in Mobile Robots",
        "summary": "We address the challenge of continual learning for mobile robots operating over extended time periods. Our method enables robots to learn new skills and environments without catastrophic forgetting of previously learned behaviors. We evaluate on a mobile robot platform deployed over six months in dynamic indoor environments.",
        "published": "2023-08-30",
        "authors": "Georgia Chalvatzaki, Jeanette Bohg, et al.",
        "link": "http://arxiv.org/abs/2308.00023",
        "primary_category": "cs.RO"
    },
    {
        "title": "Point Cloud-Based Object Manipulation with Graph Neural Networks",
        "summary": "We present a point cloud-based manipulation framework using graph neural networks to process 3D scene representations. Our method directly operates on raw point cloud observations to predict grasp affordances and manipulation trajectories, eliminating the need for explicit object mesh reconstruction.",
        "published": "2023-07-12",
        "authors": "Charles Qi, Leonidas Guibas, et al.",
        "link": "http://arxiv.org/abs/2307.00024",
        "primary_category": "cs.CV"
    },
    {
        "title": "Socially Aware Navigation for Service Robots in Crowded Environments",
        "summary": "This paper proposes a socially aware navigation framework for service robots operating in crowded human environments. Our approach models human motion prediction and social norms using deep learning, enabling the robot to navigate in a manner that is both efficient and socially compliant.",
        "published": "2023-06-05",
        "authors": "Henny Admoni, Siddhartha Srinivasa, et al.",
        "link": "http://arxiv.org/abs/2306.00025",
        "primary_category": "cs.RO"
    },
    {
        "title": "Composable Skill Learning for Hierarchical Robot Control",
        "summary": "We develop a composable skill learning framework that enables robots to acquire reusable motor skills and compose them hierarchically to solve complex long-horizon tasks. Our approach uses option frameworks with learned termination conditions and skill initiation classifiers trained from demonstration data.",
        "published": "2023-05-18",
        "authors": "Doina Precup, Doina Precup, et al.",
        "link": "http://arxiv.org/abs/2305.00026",
        "primary_category": "cs.AI"
    },
    {
        "title": "Domain-Adaptive Sim-to-Real Transfer Using Cycle-Consistent Latent Spaces",
        "summary": "We propose a domain adaptation method for sim-to-real transfer that learns cycle-consistent latent spaces aligning simulation and real-world observations. Our approach enables zero-shot policy transfer without requiring real-world fine-tuning, validated on quadruped locomotion and manipulation tasks.",
        "published": "2023-04-22",
        "authors": "Kate Saenko, Kuniaki Saito, et al.",
        "link": "http://arxiv.org/abs/2304.00027",
        "primary_category": "cs.RO"
    },
    {
        "title": "Self-Supervised Visual Representation Learning for Robotic Manipulation",
        "summary": "This work investigates self-supervised learning methods for acquiring visual representations suitable for robotic manipulation. We compare contrastive learning, masked autoencoding, and predictive coding approaches on manipulation benchmarks, identifying key factors that lead to transferable visual features for downstream control tasks.",
        "published": "2023-03-10",
        "authors": "Lerrel Pinto, Abhinav Gupta, et al.",
        "link": "http://arxiv.org/abs/2303.00028",
        "primary_category": "cs.CV"
    },
    {
        "title": "Reactive Planning for Dynamic Manipulation Under Uncertainty",
        "summary": "We present a reactive planning framework for dynamic manipulation tasks involving moving objects and uncertain physics parameters. Our method combines online trajectory optimization with learned dynamics models to adapt plans in real-time based on visual feedback, achieving robust performance on catching and throwing tasks.",
        "published": "2023-02-14",
        "authors": "Tamas Lozano-Perez, Leslie Kaelbling, et al.",
        "link": "http://arxiv.org/abs/2302.00029",
        "primary_category": "cs.RO"
    },
    {
        "title": "Bimanual Coordination for Complex Assembly Tasks Using Shared Autonomy",
        "summary": "We address bimanual coordination for complex assembly tasks using a shared autonomy framework. Our system learns to predict human intent from partial task demonstrations and provides assistance that adapts to the operator's skill level. Results on furniture assembly tasks show reduced completion time and cognitive load.",
        "published": "2023-01-25",
        "authors": "Julie Shah, Stefanos Nikolaidis, et al.",
        "link": "http://arxiv.org/abs/2301.00030",
        "primary_category": "cs.RO"
    },
    {
        "title": "Towards General-Purpose Robots via Large-Scale Behavioral Cloning",
        "summary": "This paper explores scaling behavioral cloning to large and diverse robot demonstration datasets. We train a single policy on data from multiple robot platforms and task domains, finding that cross-embodiment training improves generalization. The resulting model exhibits emergent capabilities not present in any single training task.",
        "published": "2022-12-08",
        "authors": "Brian Ichter, Danny Driess, et al.",
        "link": "http://arxiv.org/abs/2212.00031",
        "primary_category": "cs.AI"
    },
    {
        "title": "Active Perception for Object Search in Cluttered Environments",
        "summary": "We develop an active perception approach for object search that decides both where to look and how to manipulate clutter. Our method uses a belief representation over object locations and plans information-gathering actions that reduce uncertainty. Experiments demonstrate efficient search in highly cluttered scenes.",
        "published": "2022-11-15",
        "authors": "Andreas Geiger, Jennette Bohg, et al.",
        "link": "http://arxiv.org/abs/2211.00032",
        "primary_category": "cs.RO"
    },
    {
        "title": "Learning Contact-Rich Skills from Demonstration with Differentiable Physics",
        "summary": "We propose a learning from demonstration method that leverages differentiable physics simulation to optimize manipulation skills involving rich contact interactions. Our approach backpropagates through the physics engine to refine demonstrated trajectories, achieving smooth and physically plausible behaviors.",
        "published": "2022-10-20",
        "authors": "Miles Macklin, Matthias Muller, et al.",
        "link": "http://arxiv.org/abs/2210.00033",
        "primary_category": "cs.RO"
    },
    {
        "title": "Vision-Language Pretraining for Robotic Task Planning",
        "summary": "This work investigates using vision-language pretrained models for zero-shot robotic task planning. We extract action plans from large language models grounded in visual scene understanding, enabling robots to execute complex multi-step tasks described in natural language without task-specific training.",
        "published": "2022-09-12",
        "authors": "Yuke Zhu, Li Fei-Fei, et al.",
        "link": "http://arxiv.org/abs/2209.00034",
        "primary_category": "cs.AI"
    },
    {
        "title": "Whole-Body Control of Humanoid Robots Through Learned Momentum Tasks",
        "summary": "We present a whole-body control framework for humanoid robots that uses learned momentum tasks to coordinate upper and lower body motion. Our method automatically generates appropriate stepping and reaching motions for dynamic balance and manipulation, evaluated on a full-size humanoid robot.",
        "published": "2022-08-05",
        "authors": "Ludovic Righetti, Jemin Hwangbo, et al.",
        "link": "http://arxiv.org/abs/2208.00035",
        "primary_category": "cs.RO"
    },
    {
        "title": "Deformable Object Manipulation with Differentiable Simulation and Control",
        "summary": "We address deformable object manipulation by combining differentiable simulation with model predictive control. Our approach learns material parameters online and uses them to plan manipulation strategies for cloth folding, rope manipulation, and soft object positioning tasks.",
        "published": "2022-07-18",
        "authors": "David Held, Yunzhu Li, et al.",
        "link": "http://arxiv.org/abs/2207.00036",
        "primary_category": "cs.RO"
    },
    {
        "title": "Multi-Robot Coordination for Collaborative Object Transport",
        "summary": "This paper presents a multi-robot coordination algorithm for collaborative transport of large objects. Our method uses distributed optimization to allocate forces among robots while maintaining grasp stability and collision avoidance. Experiments demonstrate transport of objects requiring 4+ robots on uneven terrain.",
        "published": "2022-06-22",
        "authors": "Vijay Kumar, Mark Yim, et al.",
        "link": "http://arxiv.org/abs/2206.00037",
        "primary_category": "cs.RO"
    },
    {
        "title": "Learning to Walk in Minutes: Efficient Quadruped Locomotion via Meta-Reinforcement Learning",
        "summary": "We demonstrate that quadruped robots can learn to walk in just minutes of real-world experience using meta-reinforcement learning. Our method meta-trains a policy prior in simulation that enables rapid adaptation to new terrains and robot hardware parameters with minimal online interaction.",
        "published": "2022-05-30",
        "authors": "Pulkit Agrawal, Ashish Kumar, et al.",
        "link": "http://arxiv.org/abs/2205.00038",
        "primary_category": "cs.RO"
    },
    {
        "title": "Temporal Abstraction in Robot Skill Learning with Options Framework",
        "summary": "We investigate temporal abstraction for robot skill learning using the options framework. Our approach automatically discovers useful subgoal states and learns corresponding option policies, enabling efficient learning of long-horizon manipulation tasks through hierarchical composition of skills.",
        "published": "2022-04-14",
        "authors": "Richard Sutton, Doina Precup, et al.",
        "link": "http://arxiv.org/abs/2204.00039",
        "primary_category": "cs.AI"
    },
    {
        "title": "Tactile Exploration for Object Recognition and Pose Estimation",
        "summary": "This work explores active tactile exploration strategies for object recognition and pose estimation. Our method learns to select touch locations that maximally reduce uncertainty about object identity and pose, achieving accurate recognition with fewer touches than passive or random exploration.",
        "published": "2022-03-08",
        "authors": "Nathan Lepora, Robert Dahiya, et al.",
        "link": "http://arxiv.org/abs/2203.00040",
        "primary_category": "cs.RO"
    },
    {
        "title": "Real-Time Motion Planning for High-DOF Robots Using Neural Proximity Queries",
        "summary": "We present a real-time motion planning method for high-degree-of-freedom robots using neural network-based proximity queries. Our approach replaces expensive collision checking with learned approximations, enabling planning rates of 1000+ Hz for 7-DOF arms in cluttered environments.",
        "published": "2022-02-20",
        "authors": "Ken Goldberg, Jeffrey Ichnowski, et al.",
        "link": "http://arxiv.org/abs/2202.00041",
        "primary_category": "cs.RO"
    },
    {
        "title": "Cross-Embodiment Learning: Training Policies That Transfer Across Different Robot Morphologies",
        "summary": "We study cross-embodiment learning, where policies trained on one robot morphology transfer to different morphologies. Our method learns embodiment-invariant state representations and action abstractions that enable zero-shot transfer between manipulators with varying numbers of joints and link lengths.",
        "published": "2022-01-12",
        "authors": "Pieter Abbeel, Chelsea Finn, et al.",
        "link": "http://arxiv.org/abs/2201.00042",
        "primary_category": "cs.AI"
    },
    {
        "title": "Embodied Question Answering in Photorealistic Environments with Hybrid Computing",
        "summary": "We address embodied question answering in photorealistic 3D environments using a hybrid computing approach that combines neural perception with symbolic reasoning. Our system navigates environments to gather visual information and answers questions requiring multi-step reasoning about object properties and relationships.",
        "published": "2021-12-05",
        "authors": "Manolis Savva, Abhishek Das, et al.",
        "link": "http://arxiv.org/abs/2112.00043",
        "primary_category": "cs.CV"
    },
    {
        "title": "Learning Manipulation Skills from Human Videos via Implicit 3D Understanding",
        "summary": "We propose a method for learning robot manipulation skills by watching human demonstration videos. Our approach infers implicit 3D understanding from 2D video and transfers the inferred action parameters to robot execution, enabling learning of diverse skills without robot demonstrations.",
        "published": "2021-11-18",
        "authors": "Abhinav Gupta, Shubham Tulsiani, et al.",
        "link": "http://arxiv.org/abs/2111.00044",
        "primary_category": "cs.CV"
    },
    {
        "title": "Energy-Efficient Locomotion for Bipedal Robots via Passive Dynamics",
        "summary": "This paper investigates energy-efficient bipedal locomotion inspired by passive dynamic walking principles. We design controllers that exploit natural dynamics of the robot mechanism, achieving human-like energy efficiency while maintaining robustness to perturbations on a 3D bipedal robot.",
        "published": "2021-10-25",
        "authors": "Andy Ruina, Steven Collins, et al.",
        "link": "http://arxiv.org/abs/2110.00045",
        "primary_category": "cs.RO"
    },
    {
        "title": "Scene Graph Generation for Robot Task Planning: A Review and New Directions",
        "summary": "We review methods for scene graph generation and their application to robot task planning. Our analysis covers visual scene understanding, relational reasoning, and graph-based planning, and identifies opportunities for integrating large language models with structured scene representations for more capable robot planners.",
        "published": "2021-09-14",
        "authors": "Jia Deng, Ranjay Krishna, et al.",
        "link": "http://arxiv.org/abs/2109.00046",
        "primary_category": "cs.CV"
    },
    {
        "title": "Safe Learning-Based Control with Control Barrier Functions and Gaussian Processes",
        "summary": "We combine control barrier functions with Gaussian process dynamics models for safe learning-based control. Our approach provides probabilistic safety guarantees during online learning of uncertain dynamics, demonstrated on a cart-pole system and a quadrotor navigating near obstacles.",
        "published": "2021-08-30",
        "authors": "Aaron Ames, Koushil Sreenath, et al.",
        "link": "http://arxiv.org/abs/2108.00047",
        "primary_category": "cs.SY"
    },
    {
        "title": "Grasping in the Wild: Learning 6DoF Grasp Detection from Unlabelled RGB-D Data",
        "summary": "We present a self-supervised method for learning 6-degree-of-freedom grasp detection from unlabeled RGB-D images collected in real-world environments. Our approach uses grasp trial outcomes as supervision signals, progressively improving grasp success rates without human annotation.",
        "published": "2021-07-12",
        "authors": "Dieter Fox, Andreas ten Pas, et al.",
        "link": "http://arxiv.org/abs/2107.00048",
        "primary_category": "cs.RO"
    },
    {
        "title": "Human-Robot Handover: A Survey of Recent Advances and Open Problems",
        "summary": "This survey reviews recent advances in human-robot handover interaction. We categorize approaches by grasp planning, motion prediction, intent recognition, and social signal processing, and identify challenges including natural timing, force adaptation, and handling of unexpected situations.",
        "published": "2021-06-05",
        "authors": "Yu Sun, Heni Ben Amor, et al.",
        "link": "http://arxiv.org/abs/2106.00049",
        "primary_category": "cs.RO"
    },
    {
        "title": "Learning to Manipulate Tools by Combining Simulation and Real-World Experience",
        "summary": "We propose a tool manipulation learning framework that combines physics simulation with real-world experience. Our method uses simulation to explore diverse tool-use strategies and real-world execution to refine strategies that transfer successfully, demonstrated on hammering, screwing, and cutting tasks.",
        "published": "2021-05-18",
        "authors": "Jiajun Wu, Katerina Fragkiadaki, et al.",
        "link": "http://arxiv.org/abs/2105.00050",
        "primary_category": "cs.RO"
    },
    {
        "title": "Imitation Learning from Observation: A Review and Analysis of Design Choices",
        "summary": "We provide a comprehensive review of imitation learning from observation, where agents learn behaviors from state-only demonstrations without action labels. Our analysis covers algorithmic design choices, representation learning strategies, and theoretical properties, with recommendations for practical application.",
        "published": "2021-04-22",
        "authors": "Faraz Torabi, Garrett Warnell, et al.",
        "link": "http://arxiv.org/abs/2104.00051",
        "primary_category": "cs.AI"
    },
    {
        "title": "Dynamic Grasping with Multi-Fingered Hands Using Tactile Feedback and Reinforcement Learning",
        "summary": "We develop a dynamic grasping approach for multi-fingered hands that uses high-resolution tactile feedback within a reinforcement learning framework. Our method learns to modulate grasp forces and finger configurations in response to slip detection, achieving robust grasping of fragile and deformable objects.",
        "published": "2021-03-10",
        "authors": "Veronica Santos, Zhe Su, et al.",
        "link": "http://arxiv.org/abs/2103.00052",
        "primary_category": "cs.RO"
    },
    {
        "title": "Navigation in Unseen Environments with Learned Spatial Priors",
        "summary": "We address visual navigation in previously unseen environments by leveraging learned spatial priors from large-scale training. Our approach predicts navigable spaces and goal locations from partial observations, enabling efficient exploration and goal-directed navigation without environment-specific training.",
        "published": "2021-02-14",
        "authors": "Dhruv Batra, Manolis Savva, et al.",
        "link": "http://arxiv.org/abs/2102.00053",
        "primary_category": "cs.CV"
    },
    {
        "title": "Soft Robot Design and Control: A Survey of Bio-Inspired Approaches",
        "summary": "This survey reviews bio-inspired approaches to soft robot design and control. We cover continuum manipulators, pneumatic actuators, and variable stiffness mechanisms, examining how biological principles such as muscular hydrostats and octopus arms inform robot design and control strategies.",
        "published": "2021-01-25",
        "authors": "Cecilia Laschi, Daniela Rus, et al.",
        "link": "http://arxiv.org/abs/2101.00054",
        "primary_category": "cs.RO"
    },
    {
        "title": "Foundation Models Meet Robotics: Opportunities for Large Pretrained Models in Robot Learning",
        "summary": "We explore how large pretrained foundation models can accelerate robot learning. Our analysis covers vision encoders, language models, and multimodal models, examining methods for adaptation to robotic control and identifying key challenges in bridging the gap between internet-scale pretraining and embodied intelligence.",
        "published": "2023-04-01",
        "authors": "OpenAI Robotics Team",
        "link": "http://arxiv.org/abs/2304.00055",
        "primary_category": "cs.AI"
    },
    {
        "title": "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control",
        "summary": "We present RT-2, a family of vision-language-action models that incorporate web-scale vision-language pretraining into robotic control. Our models achieve generalization to novel objects, backgrounds, and instructions far beyond the training distribution, demonstrating the value of internet knowledge for robot learning.",
        "published": "2023-07-01",
        "authors": "Google DeepMind Robotics Team",
        "link": "http://arxiv.org/abs/2307.00056",
        "primary_category": "cs.RO"
    },
    {
        "title": "Eureka: Human-Level Reward Design via Coding Large Language Models",
        "summary": "We introduce Eureka, a framework that uses large language models to generate reward functions for reinforcement learning. Our method achieves human-level reward design on diverse tasks including dexterous manipulation and locomotion, surpassing expert-engineered rewards on multiple benchmarks.",
        "published": "2023-10-01",
        "authors": "NVIDIA AI Research",
        "link": "http://arxiv.org/abs/2310.00057",
        "primary_category": "cs.AI"
    },
    {
        "title": "Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition",
        "summary": "We present a framework for scaling robot skill acquisition using natural language guidance. Our method collects diverse demonstration data across many tasks and uses language to structure and distill knowledge into generalizable skills. The resulting policy handles thousands of instruction variants.",
        "published": "2023-11-01",
        "authors": "Google Research",
        "link": "http://arxiv.org/abs/2311.00058",
        "primary_category": "cs.RO"
    },
    {
        "title": "Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation",
        "summary": "We present Mobile ALOHA, a low-cost whole-body teleoperation system for collecting bimanual mobile manipulation data. Using this system, we collect large-scale demonstration datasets and train policies that enable a mobile manipulator to perform complex household tasks with high success rates.",
        "published": "2024-01-01",
        "authors": "Stanford ILIAD Lab",
        "link": "http://arxiv.org/abs/2401.00059",
        "primary_category": "cs.RO"
    },
    {
        "title": "Figure AI Humanoid Control: Learning Whole-Body Behaviors for Humanoid Robots",
        "summary": "We describe the learning-based control system developed for the Figure humanoid robot. Our approach combines reinforcement learning in simulation with real-world adaptation to achieve dynamic locomotion and manipulation behaviors on a full-size humanoid robot designed for practical applications.",
        "published": "2024-03-01",
        "authors": "Figure AI Research Team",
        "link": "http://arxiv.org/abs/2403.00060",
        "primary_category": "cs.RO"
    },
    {
        "title": "Tesla Optimus: From Simulation to Real-World Humanoid Control",
        "summary": "We detail the development of control policies for the Tesla Optimus humanoid robot. Our pipeline includes large-scale simulation training, sim-to-real transfer techniques, and iterative real-world refinement. The resulting system demonstrates robust walking, object manipulation, and factory task execution.",
        "published": "2024-05-01",
        "authors": "Tesla AI Team",
        "link": "http://arxiv.org/abs/2405.00061",
        "primary_category": "cs.RO"
    },
    {
        "title": "Boston Dynamics Atlas: Advanced Locomotion and Manipulation for Humanoid Robotics",
        "summary": "We present recent advances in the Atlas humanoid robot's control system. Our work focuses on dynamic athletic behaviors including running, jumping, and manipulating heavy objects while maintaining balance. We discuss the underlying trajectory optimization and state estimation algorithms.",
        "published": "2024-02-01",
        "authors": "Boston Dynamics Research",
        "link": "http://arxiv.org/abs/2402.00062",
        "primary_category": "cs.RO"
    },
    {
        "title": "Unitree H1: Low-Cost High-Performance Humanoid Robot Platform",
        "summary": "We introduce the Unitree H1 humanoid robot, designed as an affordable yet capable platform for embodied AI research. We describe the mechanical design, actuator selection, and baseline control policies that enable stable locomotion and basic manipulation at a fraction of the cost of existing platforms.",
        "published": "2024-04-01",
        "authors": "Unitree Robotics",
        "link": "http://arxiv.org/abs/2404.00063",
        "primary_category": "cs.RO"
    },
    {
        "title": "AgiBot World: A Large-Scale Platform for Embodied AI Development",
        "summary": "We present AgiBot World, a comprehensive platform for embodied AI research and development. The platform includes a humanoid robot, simulation environment, dataset collection pipeline, and training framework. We release datasets and pretrained models to accelerate research in general-purpose robotics.",
        "published": "2024-06-01",
        "authors": "AgiBot Research Team",
        "link": "http://arxiv.org/abs/2406.00064",
        "primary_category": "cs.RO"
    },
    {
        "title": "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion",
        "summary": "We introduce diffusion policy, a new representation for visuomotor policies based on denoising diffusion probabilistic models. Our approach models the distribution of actions conditioned on observations, enabling multimodal behavior expression and improved performance on complex manipulation tasks.",
        "published": "2023-03-01",
        "authors": "Columbia Robotics Lab",
        "link": "http://arxiv.org/abs/2303.00065",
        "primary_category": "cs.RO"
    },
    {
        "title": "Improving Sim-to-Real Transfer via Procedural Domain Randomization",
        "summary": "We propose procedural domain randomization for improved sim-to-real transfer. Our method generates diverse training environments using procedural content generation, exposing policies to a wider distribution of visual and physical properties than manual randomization strategies.",
        "published": "2023-06-01",
        "authors": "Unity AI Research",
        "link": "http://arxiv.org/abs/2306.00066",
        "primary_category": "cs.RO"
    },
    {
        "title": "Learning Visual Servoing with Deep Feature Points",
        "summary": "We develop a visual servoing approach that uses deep learning to detect stable and trackable feature points. Our method combines learned feature detection with classical visual servoing control, achieving robust positioning accuracy under varying lighting conditions and partial occlusions.",
        "published": "2023-08-01",
        "authors": "Francois Chaumette, et al.",
        "link": "http://arxiv.org/abs/2308.00067",
        "primary_category": "cs.CV"
    },
    {
        "title": "Tool-Augmented Language Models for Robot Task Planning",
        "summary": "We augment large language models with external tools for robot task planning. Our system can query object properties, check reachability, and verify constraints during plan generation, producing executable plans that respect robot capabilities and environmental constraints.",
        "published": "2023-09-01",
        "authors": "Shimon Whiteson, et al.",
        "link": "http://arxiv.org/abs/2309.00068",
        "primary_category": "cs.AI"
    },
    {
        "title": "Sample-Efficient Reinforcement Learning for Robot Manipulation via Offline-to-Online Adaptation",
        "summary": "We propose an offline-to-online reinforcement learning method for sample-efficient robot manipulation. Our approach pretrains policies on offline demonstration datasets and fine-tunes with limited online interaction, achieving high performance with orders of magnitude less real-world data than standard online RL.",
        "published": "2023-12-01",
        "authors": "Sergey Levine, et al.",
        "link": "http://arxiv.org/abs/2312.00069",
        "primary_category": "cs.LG"
    },
    {
        "title": "Learning Robot Skills from Human Preferences: A Survey",
        "summary": "We survey methods for learning robot skills from human preferences, including reward learning from comparisons, ranking-based feedback, and natural language critiques. Our analysis covers algorithmic approaches, data collection strategies, and applications across manipulation, locomotion, and human-robot interaction.",
        "published": "2024-07-01",
        "authors": "Dorsa Sadigh, et al.",
        "link": "http://arxiv.org/abs/2407.00070",
        "primary_category": "cs.RO"
    },
    {
        "title": "Object-Centric Representations for Robot Learning: A Review",
        "summary": "We review object-centric representation learning methods for robot manipulation. Our survey covers slot-based attention, compositional generative models, and neural scene representations, analyzing their benefits for generalization, transfer learning, and few-shot adaptation in robotic tasks.",
        "published": "2024-08-01",
        "authors": "Bernhard Scholkopf, et al.",
        "link": "http://arxiv.org/abs/2408.00071",
        "primary_category": "cs.CV"
    },
    {
        "title": "Neural Radiance Fields for Robot Perception and Planning",
        "summary": "We investigate the application of Neural Radiance Fields (NeRF) to robot perception and planning. Our work demonstrates how NeRF representations enable accurate 3D scene understanding, collision-free motion planning, and view-based task verification from limited camera observations.",
        "published": "2024-09-01",
        "authors": "Angjoo Kanazawa, et al.",
        "link": "http://arxiv.org/abs/2409.00072",
        "primary_category": "cs.CV"
    },
    {
        "title": "Offline Model-Based Reinforcement Learning for Contact-Rich Manipulation",
        "summary": "We develop an offline model-based reinforcement learning method for contact-rich manipulation tasks. Our approach learns a dynamics model from offline data and uses it for planning, with uncertainty-aware model predictions enabling safe and effective behavior in scenarios with complex contact dynamics.",
        "published": "2024-10-01",
        "authors": "Marc Deisenroth, et al.",
        "link": "http://arxiv.org/abs/2410.00073",
        "primary_category": "cs.LG"
    },
    {
        "title": "Generalizable Manipulation Primitives via Task and Motion Planning",
        "summary": "We present a framework for learning generalizable manipulation primitives using task and motion planning. Our method defines reusable manipulation skills parameterized by object properties and task constraints, enabling composition into complex multi-object manipulation behaviors.",
        "published": "2024-11-01",
        "authors": "Leslie Kaelbling, Tomas Lozano-Perez, et al.",
        "link": "http://arxiv.org/abs/2411.00074",
        "primary_category": "cs.RO"
    },
    {
        "title": "Vision-Language Models for Robot Affordance Detection",
        "summary": "We investigate using vision-language pretrained models for affordance detection in robotic manipulation. Our approach leverages the alignment between visual regions and semantic concepts to identify object parts suitable for grasping, pushing, and other manipulation actions without task-specific training.",
        "published": "2024-12-01",
        "authors": "Ross Girshick, et al.",
        "link": "http://arxiv.org/abs/2412.00075",
        "primary_category": "cs.CV"
    },
    {
        "title": "Tactile-Based In-Hand Manipulation with Underactuated Hands",
        "summary": "We address in-hand manipulation with underactuated hands using tactile feedback. Our method learns to reposition objects within the hand by modulating actuator commands based on tactile sensor arrays, achieving versatile manipulation despite limited degrees of freedom.",
        "published": "2025-01-01",
        "authors": "Aaron Dollar, et al.",
        "link": "http://arxiv.org/abs/2501.00076",
        "primary_category": "cs.RO"
    },
    {
        "title": "Long-Horizon Task Planning with Abstract World Models",
        "summary": "We propose abstract world models for long-horizon task planning in robotics. Our approach learns hierarchical state abstractions that enable efficient planning over extended time horizons, with experiments demonstrating complex multi-step tasks requiring dozens of primitive actions.",
        "published": "2025-02-01",
        "authors": "Yoshua Bengio, et al.",
        "link": "http://arxiv.org/abs/2502.00077",
        "primary_category": "cs.AI"
    },
    {
        "title": "Learning Adaptive Behaviors for Human-Robot Collaboration",
        "summary": "We develop methods for learning adaptive behaviors in human-robot collaborative tasks. Our approach models human behavior patterns and adapts robot assistance strategies in real-time, improving task efficiency and user satisfaction in shared workspace scenarios.",
        "published": "2025-03-01",
        "authors": "Julie Shah, et al.",
        "link": "http://arxiv.org/abs/2503.00078",
        "primary_category": "cs.RO"
    },
    {
        "title": "Real-Time Object Tracking for Robot Manipulation Under Dynamic Scenes",
        "summary": "We present a real-time object tracking system for robot manipulation in dynamic scenes. Our method combines visual tracking with motion prediction to maintain accurate object poses even under occlusion and rapid motion, enabling reliable grasping of moving objects.",
        "published": "2025-04-01",
        "authors": "Antonio Torralba, et al.",
        "link": "http://arxiv.org/abs/2504.00079",
        "primary_category": "cs.CV"
    },
    {
        "title": "Composable Robot Behaviors via Program Synthesis from Demonstrations",
        "summary": "We propose a program synthesis approach for learning composable robot behaviors from demonstrations. Our method extracts reusable behavior primitives and compositional rules from human demonstrations, generating interpretable programs that generalize to new task configurations.",
        "published": "2025-05-01",
        "authors": "Armando Solar-Lezama, et al.",
        "link": "http://arxiv.org/abs/2505.00080",
        "primary_category": "cs.AI"
    },
    {
        "title": "Self-Calibrating Visual Servoing for Industrial Robot Arms",
        "summary": "We develop a self-calibrating visual servoing system for industrial robot arms. Our method automatically estimates camera parameters and hand-eye transformations during operation, eliminating the need for manual calibration and maintaining accuracy despite mechanical wear and thermal effects.",
        "published": "2025-06-01",
        "authors": "Peter Corke, et al.",
        "link": "http://arxiv.org/abs/2506.00081",
        "primary_category": "cs.RO"
    },
    {
        "title": "Learning Energy-Efficient Gait Patterns for Bipedal Robots via Optimal Control",
        "summary": "We address energy-efficient gait generation for bipedal robots using trajectory optimization. Our approach formulates gait design as an optimal control problem with energy cost terms, producing natural and efficient walking patterns validated on a physical humanoid platform.",
        "published": "2025-07-01",
        "authors": "Katja Mombaur, et al.",
        "link": "http://arxiv.org/abs/2507.00082",
        "primary_category": "cs.RO"
    },
    {
        "title": "Robust Grasp Planning Under Shape Uncertainty Using Gaussian Process Implicit Surfaces",
        "summary": "We propose a grasp planning method that explicitly models shape uncertainty using Gaussian process implicit surfaces. Our approach generates grasps that are robust to shape estimation errors, with experiments showing improved success rates when manipulating objects with incomplete or noisy geometric models.",
        "published": "2025-08-01",
        "authors": "Ken Goldberg, et al.",
        "link": "http://arxiv.org/abs/2508.00083",
        "primary_category": "cs.RO"
    },
    {
        "title": "Multi-Agent Reinforcement Learning for Coordinated Robot Teams",
        "summary": "We develop multi-agent reinforcement learning algorithms for coordinated robot teams. Our methods address credit assignment, communication, and emergent coordination in teams of heterogeneous robots, with applications to collaborative construction, search and rescue, and warehouse logistics.",
        "published": "2025-09-01",
        "authors": "Peter Stone, et al.",
        "link": "http://arxiv.org/abs/2509.00084",
        "primary_category": "cs.AI"
    },
    {
        "title": "Learning Predictive Models for Deformable Object Manipulation",
        "summary": "We learn predictive models for deformable object manipulation using graph neural networks. Our approach predicts the effects of manipulator actions on cloth, rope, and soft objects, enabling model-based planning for complex deformation tasks such as folding and knot tying.",
        "published": "2025-10-01",
        "authors": "David Held, et al.",
        "link": "http://arxiv.org/abs/2510.00085",
        "primary_category": "cs.RO"
    },
    {
        "title": "Neural Task Programming: Learning to Compose Robot Skills from Natural Language",
        "summary": "We propose neural task programming, a method for composing robot skills from natural language instructions. Our system parses task descriptions into programmatic structures and grounds them in learned skill libraries, enabling execution of novel complex tasks specified in unstructured language.",
        "published": "2025-11-01",
        "authors": "Dieter Fox, et al.",
        "link": "http://arxiv.org/abs/2511.00086",
        "primary_category": "cs.AI"
    },
    {
        "title": "Tactile Sensors for Robot Manipulation: Materials, Fabrication, and Learning Algorithms",
        "summary": "We review recent advances in tactile sensing for robot manipulation. Our survey covers sensor materials and fabrication techniques, signal processing methods, and learning algorithms that leverage tactile data for grasp stability estimation, slip detection, and texture recognition.",
        "published": "2025-12-01",
        "authors": "Robert Dahiya, et al.",
        "link": "http://arxiv.org/abs/2512.00087",
        "primary_category": "cs.RO"
    },
    {
        "title": "Risk-Aware Motion Planning for Autonomous Robots in Uncertain Environments",
        "summary": "We develop risk-aware motion planning methods for autonomous robots operating in uncertain environments. Our approach quantifies risk using conditional value-at-risk and optimizes trajectories that balance efficiency with safety constraints, demonstrated on autonomous navigation and manipulation tasks.",
        "published": "2026-01-01",
        "authors": "Marco Pavone, et al.",
        "link": "http://arxiv.org/abs/2601.00088",
        "primary_category": "cs.RO"
    },
    {
        "title": "Foundation Models for Embodied Navigation: A Survey and Benchmark",
        "summary": "We survey the application of foundation models to embodied navigation tasks. Our work covers vision-language models for instruction following, pretraining strategies for navigation policies, and benchmarks for evaluating generalization across environments and task specifications.",
        "published": "2026-02-01",
        "authors": "Peter Anderson, et al.",
        "link": "http://arxiv.org/abs/2602.00089",
        "primary_category": "cs.CV"
    },
    {
        "title": "Learning to Grasp with Implicit 3D Shape Representations",
        "summary": "We propose a grasp learning approach that uses implicit 3D shape representations. Our method predicts grasp quality from neural implicit fields, enabling reasoning about object geometry and topology without explicit mesh reconstruction. Results show improved generalization to novel object categories.",
        "published": "2026-03-01",
        "authors": "Thomas Funkhouser, et al.",
        "link": "http://arxiv.org/abs/2603.00090",
        "primary_category": "cs.RO"
    },
    {
        "title": "Adaptive Control for Legged Robots on Varying Terrains via Meta-Learning",
        "summary": "We develop an adaptive control method for legged robots using meta-learning. Our approach learns a prior over terrain-adaptive control policies and quickly adapts to new terrain types with minimal experience, enabling robust locomotion on sand, gravel, grass, and rocky surfaces.",
        "published": "2026-04-01",
        "authors": "Sangbae Kim, et al.",
        "link": "http://arxiv.org/abs/2604.00091",
        "primary_category": "cs.RO"
    }
]

# 创建DataFrame并保存
df = pd.DataFrame(papers_data)
df['published'] = pd.to_datetime(df['published'])
output_path = '../data/raw/arxiv_papers.csv'
df.to_csv(output_path, index=False)
print(f"已生成 {len(df)} 篇种子论文数据，保存到 {output_path}")
print(df.head())
