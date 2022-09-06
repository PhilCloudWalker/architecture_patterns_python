import abc
import domain_package as model

class AbstractRepositoy(abc.ABC):
    @abc.abstractclassmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get(self, reference_id) -> model.Batch:
        raise NotImplementedError
