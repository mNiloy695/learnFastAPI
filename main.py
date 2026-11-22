from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

class Note(BaseModel):
    title:str
    content:str
    learned:bool

class UpdateNote(BaseModel):
    title:str|None=None
    content:str|None=None
    learned:bool|None=None

notes =[
    {
        "id": 1,
        "title": "My first note",
        "content": "This is my first note",
        "learned": True
    },
    {
        "id": 2,
        "title": "My second note",
        "content": "This is my second note",
        "learned": False
    },
    {
        "id": 3,
        "title": "My third note",
        "content": "This is my third note",
        "learned": True
    }
    ]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/notes")

def get_notes(title:str|None=None, learned:bool|None=None):
    if title and learned is not None:
        filtered_notes = [note for note in notes if title.lower() in note["title"].lower() and note["learned"] == learned]
        return filtered_notes
    elif title is not None:
        filtered_notes = [note for note in notes if title.lower() in note["title"].lower()]
        return filtered_notes
    elif learned is not None:
        filtered_notes = [note for note in notes if note["learned"] == learned]
        return filtered_notes
    return notes


@app.get("/notes/{note_id}")
def get_note(note_id:int):
    for note in notes:
        if note["id"]==note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.post("/notes",status_code=201)
def create_note(newNote:Note):
    new_note_id=1

    for note in notes:
        if note["id"]>=new_note_id:
            new_note_id=note["id"]+1

    note_dict = newNote.model_dump()
    note_dict["id"] = new_note_id
    notes.append(note_dict)
    return note_dict



@app.patch("/notes/{note_id}")

def update_note(note_id:int,changes:UpdateNote):

    for note in notes:
        if note["id"]==note_id:
            note.update(changes.model_dump(exclude_unset=True))
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}",status_code=204)
def delete_note(note_id:int):
    for note in notes:
        if note["id"]==note_id:
            notes.remove(note)
            return
    raise HTTPException(status_code=404, detail="Note not found")


