import { useState } from 'react'
import axios from 'axios'
import { Alert, Button, Card, Form, Input, Typography } from 'antd'

const { Title, Text } = Typography

// Backend URL for FastAPI
const API_BASE_URL = 'http://127.0.0.1:8000'

function AddEmployeeForm({ onEmployeeAdded }) {
  // Form data managed with useState
  const [formData, setFormData] = useState({ name: '', role: '' })
  const [submitting, setSubmitting] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  // Update local state whenever user types in an input
  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  // Submit form to FastAPI API using axios POST
  const handleSubmit = async () => {
    try {
      setSubmitting(true)
      setSuccessMessage('')
      setErrorMessage('')

      await axios.post(`${API_BASE_URL}/employees`, {
        name: formData.name.trim(),
        role: formData.role.trim(),
      })

      setSuccessMessage('Employee added successfully.')
      setFormData({ name: '', role: '' })
      if (onEmployeeAdded) {
        onEmployeeAdded()
      }
    } catch (error) {
      console.error('Failed to add employee:', error)
      setErrorMessage('Could not add employee. Please check backend and try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Card className="employee-form-card">
      <Title level={3} style={{ marginTop: 0, marginBottom: 6 }}>
        Add Employee
      </Title>
      <Text type="secondary">Fill the details and save.</Text>

      <Form layout="vertical" style={{ marginTop: 16 }} onFinish={handleSubmit}>
        <Form.Item
          label="Name"
          required
          rules={[{ required: true, message: 'Please enter employee name' }]}
        >
          <Input
            name="name"
            placeholder="Enter employee name"
            value={formData.name}
            onChange={handleChange}
          />
        </Form.Item>

        <Form.Item
          label="Role"
          required
          rules={[{ required: true, message: 'Please enter employee role' }]}
        >
          <Input
            name="role"
            placeholder="Enter employee role"
            value={formData.role}
            onChange={handleChange}
          />
        </Form.Item>

        <Button type="primary" htmlType="submit" loading={submitting}>
          Add Employee
        </Button>
      </Form>

      {successMessage && (
        <Alert
          style={{ marginTop: 16 }}
          type="success"
          showIcon
          message={successMessage}
        />
      )}

      {errorMessage && (
        <Alert
          style={{ marginTop: 16 }}
          type="error"
          showIcon
          message={errorMessage}
        />
      )}
    </Card>
  )
}

export default AddEmployeeForm
