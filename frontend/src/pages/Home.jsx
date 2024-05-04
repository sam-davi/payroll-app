import React from 'react'
import { useState, useEffect } from 'react'
import api from '../api'
import Note from '../components/Note'
import "../styles/Home.css"

const Home = () => {
  const defaultState = {
    title: "",
    content: ""
  }
  const [notes, setNotes] = useState([]);
  const [state, setState] = useState(defaultState)

  useEffect(() => {
    getNotes()
  }, [])

  const getNotes = async () => {
    try {
      const response = await api.get("/api/notes/")
      setNotes(response.data)
    } catch (error) {
      alert(error)
    }
  }

  const deleteNote = async (id) => {
    try {
      const response = await api.delete(`/api/notes/delete/${id}/`)
      if (response.status === 204) {
        alert("Note deleted successfully")
      } else {
        alert("Failed to delete note")
      }
      getNotes()
    } catch (error) {
      alert(error)
    }
  }

  const createNote = async (e) => {
    e.preventDefault()
    try {
      const response = await api.post("/api/notes/", state)
      if (response.status === 201) {
        alert("Note created successfully")
        setState(defaultState)
      } else {
        alert("Failed to create note")
      }
      getNotes()
    } catch (error) {
      alert(error)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setState((prevState) => ({...prevState, [name]: value}))
  }

  return (<>
    <div>
        <h2>Notes</h2>
        {notes.map((note) => (
            <Note
                key={note.id}
                note={note}
                onDelete={deleteNote}
            />
        ))}
    </div>
    <h2>Create a Note</h2>
    <form onSubmit={createNote}>
        <label htmlFor="title">Title:</label>
        <br />
        <input
            type="text"
            id="title"
            name="title"
            required
            value={state.title}
            onChange={handleChange}
        />
        <label htmlFor="content">Content:</label>
        <br />
        <textarea
            id="content"
            name="content"
            required
            value={state.content}
            onChange={handleChange}
        />
        <br />
        <input type="submit" value="Submit"></input>
    </form>
    </>
  )
}

export default Home