from abc import ABC, abstractmethod

from app.validation.confidence import (
    FieldPrediction,
)


class DocumentExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        document: bytes,
    ) -> list[FieldPrediction]:
        raise NotImplementedError
