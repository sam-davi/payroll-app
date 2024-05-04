import React, { useEffect, useState } from 'react'
import {Navigate} from 'react-router-dom'
import {jwtDecode} from 'jwt-decode'
import api from '../api'
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants'


const ProtectedRoute = ({children}) => {
  const [isAuthorized, setIsAuthorized] = useState(null)

  useEffect(() => {
    auth().catch(() => setIsAuthorized(false))
  }, [])

  const refreshToken = async () => {
    try {
        const response = await api.post('/api/token/refresh/', {
        refresh: localStorage.getItem(REFRESH_TOKEN)
        });
        if (response.status === 200) {
            localStorage.setItem(ACCESS_TOKEN, response.data.access)
            setIsAuthorized(true)
        } else {
            setIsAuthorized(false)
        }
    } catch (error) {
        console.log(error);
        setIsAuthorized(false);
    }
  }

  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN)
    if (!token) {
      setIsAuthorized(false)
      return
    }
    if (token) {
      const {exp} = jwtDecode(token)
      if (exp * 1000 < Date.now()) {
        await refreshToken()
      } else {
        setIsAuthorized(true)
      }
    }
  }

  if (isAuthorized === null) {
    return <div>Loading...</div>
  }

  return isAuthorized ? children : <Navigate to="/login" />
}

export default ProtectedRoute