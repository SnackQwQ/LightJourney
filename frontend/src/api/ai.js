import api from './index'

export function planTrip(params) {
  return api.post('/ai/plan', params)
}

export function generateCopywriting(tripId) {
  return api.post('/ai/copywriting', { trip_id: tripId })
}
