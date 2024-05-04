import React from 'react'
import '../styles/Note.css'

const Note = ({note, onDelete}) => {
  const formattedDate = new Date(note.created).toLocaleString("en-NZ", {
    weekday: "short",
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
  return (
    <div className='note-container'>
        <p className="note-title">{note.title}</p>
        <p className="note-content">{note.content}</p>
        <p className="note-date">{formattedDate}</p>
        <button className="delete-button" onClick={() => onDelete(note.id)}>Delete</button>
    </div>
  )
}

export default Note