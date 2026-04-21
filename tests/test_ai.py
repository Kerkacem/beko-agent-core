import os
import torch
from beko_v5_neural import BEKONet, neural_self_heal
from beko_v6_skills import BEKOSkills


def test_bekonet_forward_shapes():
    model = BEKONet()
    x = torch.randn(1,5)
    out = model(x)
    assert out.shape == (1,1)


def test_neural_self_heal_range():
    h = neural_self_heal()
    assert 0.0 <= h <= 1.0


def test_activate_known_skill():
    sk = BEKOSkills()
    assert sk.activate_skill('meta_ads') is True
