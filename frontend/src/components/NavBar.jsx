import React from 'react'
import { NavLink } from 'react-router-dom'

const NavBar = () => {
  return (
    <>
      <nav className='navbar navbar-expand-lg navbar-dark bg-dark'>
        <div className='container-fluid'>
          <NavLink className='navbar-brand' to={'/'}>Home</NavLink>
          <div className='collapse navbar-collapse' id='navbarNav'>
            <ul className='navbar-nav'>
              <li className='nav-item'>
                <NavLink className='nav-link' to={'/payroll'}>Payroll</NavLink>
              </li>
              <li className='nav-item'>
                <NavLink className='nav-link' to={'/register'}>Register</NavLink>
              </li>
              <li className='nav-item'>
                <NavLink className='nav-link' to={'/login'}>Login</NavLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  )
}

export default NavBar