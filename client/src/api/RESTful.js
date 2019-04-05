import axios from 'axios'
import config from '../config'

export default {
    getResources (commitCallback) {
      const URL = config.backendURL + '/resources'
      axios.get(URL)
        .then((response) => {
          commitCallback('setResources', response.data)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
        })
    },
    getHistory (resName, commitCallback) {
      const URL = config.backendURL + '/resource/' + resName + '/history'
      axios.get(URL)
        .then((response) => {
          commitCallback('setHistory', response.data)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
        })
    },
    //buyProducts (products, cb, errorCb) {
    //  setTimeout(() => {
    //    // simulate random checkout failure.
    //    (Math.random() > 0.5 || navigator.userAgent.indexOf('PhantomJS') > -1)
    //      ? cb()
    //      : errorCb()
    //  }, 100)
    //}
  }