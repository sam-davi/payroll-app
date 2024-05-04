import React from 'react'
import { useState, useEffect } from 'react'
import api from '../api'
import { ImCross, ImPlus } from 'react-icons/im'
// import "../styles/TaxCodes.css"

const TaxCodes = () => {
  const defaultState = {
    code: "",
    description: ""
  }
  const [taxCodes, setTaxCodes] = useState([])
  const [state, setState] = useState(defaultState)

  useEffect(() => {
    getTaxCodes()
  }, [])

  const getTaxCodes = async () => {
    try {
      const response = await api.get("/payroll/taxcodes/")
      setTaxCodes(response.data)
    } catch (error) {
      alert(error)
    }
  }

  const deleteTaxCode = async (url) => {
    try {
      const response = await api.delete(url)
      if (response.status === 204) {
        alert("Tax code deleted successfully")
      } else {
        alert("Failed to delete tax code")
      }
      getTaxCodes()
    } catch (error) {
      alert(error)
    }
  }

  const createTaxCode = async (e) => {
    e.preventDefault()
    try {
      const response = await api.post("/payroll/taxcodes/", state)
      if (response.status === 201) {
        alert("Tax code created successfully");
        setState(defaultState)
      } else {
        alert("Failed to create tax code")
      }
      getTaxCodes()
    } catch (error) {
      alert(error)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setState((prevState) => ({...prevState, [name]: value}))
  }

  return (
    <div>
      <h1>Tax Codes</h1>
      <table>
        <thead>
          <tr>
            <th>Code</th>
            <th>Description</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {taxCodes.map((taxCode) => (
            <tr key={taxCode.code}>
              <td>{taxCode.code}</td>
              <td>{taxCode.description}</td>
              <td>
                <button onClick={() => deleteTaxCode(taxCode.url)}><ImCross /></button>
              </td>
            </tr>
          ))}
          <tr key="new_code">
            <td>
              <input
                  type="text"
                  key="code"
                  name="code"
                  value={state.code}
                  onChange={handleChange}
              />
            </td>
            <td>
              <input
                  type="text"
                  key="description"
                  name="description"
                  value={state.description}
                  onChange={handleChange}
              />
            </td>
            <td>
              <button type="submit" onClick={createTaxCode}><ImPlus /></button>
            </td>
          </tr>
        </tbody>
      </table>
      
    </div>
  )
}

export default TaxCodes