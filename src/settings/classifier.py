from typing import Any, Dict, List, Optional, Sequence, Union

from src.settings.base import ExtraFieldsNotAllowedBaseModel


class ClassifierSettings(ExtraFieldsNotAllowedBaseModel):
    n_estimators: int
    max_depth: Optional[int]
    id2label: Dict[int, str]


class PredictOutput(ExtraFieldsNotAllowedBaseModel):
    sentiment: Union[str, Sequence[str]]
