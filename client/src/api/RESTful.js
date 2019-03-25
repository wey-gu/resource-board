import axios from 'axios'

export default {
    getResources (commitCallback) {
      const URL = 'http://dc.siwei.info:5000/resources'
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
      const URL = 'http://dc.siwei.info:5000/resource/' + resName + '/history'
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