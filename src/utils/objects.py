from pydantic import BaseModel,Field
from typing import List

class Analyst(BaseModel):
    affiliation: str = Field(description="Primary affiliation of the analyst")
    name: str = Field(description="Name of analyst")
    role: str = Field(description="Role of the analyst in the context of the topic")
    description: str = Field(description="Description of the analyst focus , concerns")  

    @property
    def persona(self)->str:
        return f"Name: {self.name}\n Role: {self.role}\n Description :{self.description}\n Affiliation: {self.affiliation}"

class Perspective(BaseModel):
    analysts : List[Analyst] =Field(description="Comperhensive list of analysis with thier roles and affiliation")