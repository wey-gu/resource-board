import Vue from 'vue'
import Vuex from 'vuex'
// ../api.RESTful.js imported as client
import client from '../api/RESTful'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loadedResources: null,
    loading: false,
    error: null,
    mock_states_stype: [
      {
        'ci': 'primary',
      },
      {
        'free': 'success',
      },
      {
        'occupied': 'error',
      },
      {
        'testing': 'warning',
      }
    ],
  },
  getters: {
    loadedBoard: (state) => {
      let board = {}
      // eslint-disable-next-line
      // console.log(state.loadedResources[0])
      if (state.loadedResources !== null) {
        for (let resource of state.loadedResources ) {
          // eslint-disable-next-line
          // console.log(resource.show)
          let RS = resource.state
          if (RS in board) {
            board[RS].push(resource)
          } else {
            board[RS] = [resource]
          }
        }
        // eslint-disable-next-line
        // console.log(board)
        return board
      } else {
        return null
      }

    },
    getLoading: (state) => {
      return state.loading
    }
  },
  mutations: {
    setResources (state, payload) {
      state.loadedResources = JSON.parse(payload)
      // eslint-disable-next-line
      // let test = state.loadedResources
      // eslint-disable-next-line
      // console.log(state.loadedResources)
    },
    updateResource (state, payload) {
      let updated_resource = JSON.parse(payload)
      for (let [index, resource] of state.loadedResources.entries() ) {
        if (resource.name === updated_resource.name) {
          state.loadedResources[index] = updated_resource
        }
      }
      // eslint-disable-next-line
      // console.log(state.loadedResources)
    },
    changeLoadingState (state, ifLoading) {
      state.loading = ifLoading
    },
    changeShowState (state, resourceName) {
      for (let [index, resource] of state.loadedResources.entries() ) {
        if (resource.name === resourceName) {
          state.loadedResources[index] = !resource.show
          // eslint-disable-next-line
          // console.log(index)
        }
      }
    }
  },
  actions: {
    // eslint-disable-next-line
    SOCKET_toldresource ({commit}, params) {
      // eslint-disable-next-line
      console.log(params)
      // update_board from socket.io server
      commit('updateResource', params)
    },
    getBoard ({commit}) {
      // initially fetch Board from backend
      commit('changeLoadingState', true)
      // context.commit is the callback passed to client.getResources
      client.getResources(commit)
      commit('changeLoadingState', false)
    }
  }
})