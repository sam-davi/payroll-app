import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import Pages from './pages/Pages'
import NavBar from './components/NavBar'

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Pages />
    </BrowserRouter>
  )
}

export default App
