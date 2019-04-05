const DEBUG = true
let backendURL = 'http://localhost:5000'
if (!DEBUG) {
    backendURL = 'https://dc.siwei.info:5000'
  }

export default {
    backendURL : backendURL,
  }