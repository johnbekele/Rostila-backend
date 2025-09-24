from typing import TypeVar, Generic, Optional, List, Dict, Any
from beanie import Document, PydanticObjectId
from pymongo.errors import DuplicateKeyError ,OperationFailure


DocumentType =TypeVar("DocumentType",bound=Document)

class BaseRepository(Generic[DocumentType]):
    def __init__(self,model:type[Document] ):
        self.model=model 


    #  Create document
    async def create(self,data: Dict[str ,Any]) -> DocumentType:
       try:
           document=self.model(**data)
           await document.create()
           return document
       except DuplicateKeyError as e:
           raise ValueError(f"Duplicate value error : {e}")
       
    #findOne
    async def find_one(self, **filter) -> Optional[DocumentType]:
        return await self.model.find_one(filter)
    
    # findByID
    async def find_by_ID(self,Object_id:str)-> Optional[DocumentType]:
        try:
            return await self.model.get(PydanticObjectId(Object_id))
        except Exception :
            return None

    
    #findMany
    async def find_many(self, filters: Dict [str ,Any], skip:int =0 , limit:int =100) -> List[DocumentType]:
        return await self.model.find(filter).skip(skip).limit(limit).to_list()
    
   #FindALL
    async def find_all(self,skip:int=0 ,limit:int=100)->List[DocumentType]:
        return await self.model.find_all().skip(skip).limit(limit).to_list()
    
    #UpdateByID
    async def update_one(self, Object_id: str, update_data: Dict[str,Any]) ->Optional[DocumentType]:
       try:
           data=await self.find_by_ID(Object_id)
           if not data:
               return None
           
           await data.update({"$set":update_data})

           updated_data=await self.find_by_ID(Object_id)
           return updated_data 
       
       except OperationFailure as e:
           raise RuntimeError (f"Upate Opration faild {e}")
      
           
        
    #DeleteBYID
    async def delete_By_ID(self, Object_id:str) -> bool:
        data=await self.find_by_ID(Object_id)
        if data:
            await data.delete()
            return True
        return False
     
        
