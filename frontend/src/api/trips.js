import api from './index'

export function getTrips(params = {}) {
  return api.get('/trips', { params })
}

export function createTrip(data) {
  return api.post('/trips', data)
}

export function updateTrip(id, data) {
  return api.put(`/trips/${id}`, data)
}

export function deleteTrip(id) {
  return api.delete(`/trips/${id}`)
}
