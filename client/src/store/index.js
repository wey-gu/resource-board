import Vue from 'vue'
import Vuex from 'vuex'
// ../api.RESTful.js imported as client
import client from '../api/RESTful'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    resources: [],
    loading: false,
    error: false,
  },
  getters: {
    getResByName: (state) => (name) =>{
      return state.resources(res => res.name === name)
    },
    loadedBoard: (state) => {
      let board = {}
      // eslint-disable-next-line
      // console.log(state.resources[0])
      if (state.resources !== null) {
        for (let resource of state.resources ) {
          // eslint-disable-next-line
          console.log(resource['show_details'])
          // init of local attr
          if (resource['show_details'] === undefined) {
            Vue.set(resource, 'show_details', false)
            Vue.set(resource, 'edit_dialog', false)
          }
          let resState = resource.state
          if (resState in board) {
            board[resState].push(resource)
          } else {
            board[resState] = [resource]
          }
        }
        // eslint-disable-next-line
        console.log(board)
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
      let newlength = 1
      for (let resource of JSON.parse(payload) ) {
        state.resources.splice(newlength)
        state.resources.splice(newlength - 1, 1, resource)
        newlength++
      }
      // eslint-disable-next-line
      // let test = state.resources
      // eslint-disable-next-line
      // console.log(state.resources)
    },
    updateResource (state, payload) {
      // eslint-disable-next-line
      console.log('updateResource: ' + payload)
      let updated_resource = JSON.parse(payload)
      for (let [index, resource] of state.resources.entries() ) {
        if (resource.name === updated_resource.name) {
          // eslint-disable-next-line
          console.log('before mutation:' + state.resources[index].state)
          //state.resources[index] = updated_resource
          state.resources.splice(index, 1, updated_resource)
          // eslint-disable-next-line
          console.log('after: mutation:' + state.resources[index].state)
        }
      }
      // eslint-disable-next-line
      // console.log(state.resources)
    },
    changeLoadingState (state, ifLoading) {
      state.loading = ifLoading
    },
  },
  actions: {
    // eslint-disable-next-line
    SOCKET_updateResource ({commit}, params) {
      // eslint-disable-next-line
      console.log('SOCKET_updateResource: ' + params)
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