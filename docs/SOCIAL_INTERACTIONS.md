# Social Interaction Layer

SafeCrossAI includes a social interaction layer for modeling relationships between road users at smart intersections.

This layer is designed to support future models such as:

- Social-LSTM
- Graph Neural Networks
- Graph Attention Networks
- Trajectory Transformers
- Collision-risk predictors

## Geometry

Basic geometry utilities are available from `safecrossai.social`.

```python
import numpy as np

from safecrossai.social import distance, bearing, relative_velocity

position_a = np.array([0.0, 0.0])
position_b = np.array([3.0, 4.0])

print(distance(position_a, position_b))
print(bearing(position_a, position_b))
```

## Neighbor Search

Neighbor search identifies nearby road users around a target agent.

```python
import numpy as np

from safecrossai.social import SocialAgent, find_neighbors

target = SocialAgent(agent_id="pedestrian_1", position=np.array([0.0, 0.0]))
agents = [
    SocialAgent(agent_id="cyclist_1", position=np.array([2.0, 0.0])),
    SocialAgent(agent_id="car_1", position=np.array([12.0, 0.0])),
]

neighbors = find_neighbors(target, agents, radius=5.0)
```

## Social Features

Pairwise social features can be extracted from a target agent and a neighboring agent.

```python
import numpy as np

from safecrossai.social.features import extract_social_features
from safecrossai.social import SocialAgent

target = SocialAgent(
    agent_id="pedestrian_1",
    position=np.array([0.0, 0.0]),
    velocity=np.array([1.0, 0.0]),
)
neighbor = SocialAgent(
    agent_id="cyclist_1",
    position=np.array([3.0, 4.0]),
    velocity=np.array([2.0, 0.0]),
)

features = extract_social_features(target, neighbor)
print(features.distance)
print(features.relative_speed)
```

## Time To Collision

The TTC utilities estimate collision risk under constant-velocity motion.

```python
import numpy as np

from safecrossai.social import time_to_collision, closest_point_of_approach

ttc = time_to_collision(
    position_a=np.array([0.0, 0.0]),
    velocity_a=np.array([1.0, 0.0]),
    position_b=np.array([10.0, 0.0]),
    velocity_b=np.array([-1.0, 0.0]),
    collision_radius=1.0,
)

approach = closest_point_of_approach(
    position_a=np.array([0.0, 0.0]),
    velocity_a=np.array([1.0, 0.0]),
    position_b=np.array([10.0, 0.0]),
    velocity_b=np.array([-1.0, 0.0]),
)
```

## Interaction Graphs

Interaction graphs represent agents as nodes and pairwise interactions as directed edges.

```python
import numpy as np

from safecrossai.social import SocialAgent, build_radius_interaction_graph

agents = [
    SocialAgent(
        agent_id="pedestrian_1",
        position=np.array([0.0, 0.0]),
        velocity=np.array([1.0, 0.0]),
    ),
    SocialAgent(
        agent_id="cyclist_1",
        position=np.array([2.0, 0.0]),
        velocity=np.array([0.0, 0.0]),
    ),
]

graph = build_radius_interaction_graph(agents, radius=5.0)
print(graph.nodes)
print(graph.edges)
```

## Unified Scene Representation

A `Scene` stores agents, timestamp, scene id, and metadata in a common format that future models can share.

```python
import numpy as np

from safecrossai.social import SocialAgent, make_scene

scene = make_scene(
    scene_id="intersection_001",
    timestamp=12.5,
    agents=[
        SocialAgent(
            agent_id="pedestrian_1",
            position=np.array([0.0, 0.0]),
            velocity=np.array([1.0, 0.0]),
        ),
        SocialAgent(
            agent_id="cyclist_1",
            position=np.array([2.0, 0.0]),
            velocity=np.array([0.0, 0.0]),
        ),
    ],
    metadata={"location": "smart_intersection_a"},
)

graph = scene.build_interaction_graph(radius=5.0)
print(scene.agent_ids())
print(graph.edges)
```

## Research Role

The social interaction layer is the bridge between trajectory prediction and road-safety reasoning. It provides the primitives needed for:

- neighbor-aware prediction,
- social pooling,
- graph construction,
- collision-risk estimation,
- infrastructure-assisted prediction at smart intersections,
- unified scene inputs for future Social-LSTM, GNN, Transformer, and Diffusion models.
