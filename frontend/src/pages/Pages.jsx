import React from 'react'
import { Routes, Route, useLocation, Navigate } from 'react-router-dom'
import NotFound from './NotFound'
import Login from './Login'
import Home from './Home'
import Register from './Register'
import TaxCodes from './TaxCodes'
import ProtectedRoute from '../components/ProtectedRoute'
import { AnimatePresence } from 'framer-motion'

function Logout() {
    localStorage.clear()
    return (
      <Navigate to="/login" />
    )
  }
  
  function RegisterAndLogout() {
    localStorage.clear()
    return (
      <Register />
    )
  }

const Pages = () => {
  const location = useLocation()
  return (
    <AnimatePresence mode='wait'>
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/payroll/taxcodes" element={<ProtectedRoute><TaxCodes /></ProtectedRoute>} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AnimatePresence>
  )
}

export default Pages