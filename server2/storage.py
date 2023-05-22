from typing import Type

from google.cloud import firestore
from pydantic import BaseModel


class StorageController:
    def __init__(self):
        self.client = firestore.Client(project="zhunium-990719")

    def _get_coll(self, model_cls: Type[BaseModel]):
        return self.client.collection(
            'SMM2' + model_cls.__name__
        )

    def _get_ref(self, model_cls: Type[BaseModel], doc_id):
        return self._get_coll(model_cls).document(doc_id)

    def get(self, model_cls: Type[BaseModel], doc_id):
        doc_ref = self._get_ref(model_cls, doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return model_cls.parse_obj(doc.to_dict())

    def get_list(self, model_cls: Type[BaseModel]):
        collection = self._get_coll(model_cls)
        return [
            model_cls.parse_obj(doc.to_dict())
            for doc in collection.stream()
        ]

    def save(self, model: BaseModel):
        doc_ref = self._get_ref(type(model), model.id)
        doc_ref.set(model.dict(), merge=True)
