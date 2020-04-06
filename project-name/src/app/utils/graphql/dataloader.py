from promise import Promise
from promise.dataloader import DataLoader


class ModelLoader(DataLoader):
    def __init__(self, model):
        super().__init__()
        self.model_class = model

    def batch_load_fn(self, keys):
        return Promise.resolve(self.model_class.objects.filter(id__in=keys))