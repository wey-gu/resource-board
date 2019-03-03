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
    histories: {},
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
          // console.log(resource['show_details'])
          // initiate local attr
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
        // console.log("[DEBUG] getters.loadedBoard:\n\t" + board)
        return board
      } else {
        return null
      }
    },
    getLoading: (state) => {
      return state.loading
    },
    getHistoryByName: (state) => (name) =>{
      if (state.histories === null) {
        return {}
      } else {
        return state.histories[name]
      }
    }
  },
  mutations: {
    setResources (state, payload) {
      // someArray.splice(start, deleteCount, item1, item2, ...)
      state.resources.splice(0, state.resources.length, ...JSON.parse(payload))
      // eslint-disable-next-line
      // console.log("[DEBUG] setResources: " + state.resources)
    },
    setHistory (state, payload) {
      let parsedPayload = JSON.parse(payload)
      let name = Object.keys(parsedPayload)[0]
      Vue.set(state.histories, name, parsedPayload[name])
    },
    updateResource (state, payload) {
      // eslint-disable-next-line
      console.log('[DEBUG] updateResource payload:\n\t' + payload)
      let updated_resource = JSON.parse(payload)
      for (let [index, resource] of state.resources.entries() ) {
        if (resource.name === updated_resource.name) {
          // eslint-disable-next-line
          console.log('[DEBUG] updateResource before mutation:\n\t' + state.resources[index].state)
          //state.resources[index] = updated_resource
          state.resources.splice(index, 1, updated_resource)
          // eslint-disable-next-line
          console.log('[DEBUG] updateResource after: mutation:\n\t' + state.resources[index].state)
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
      console.log('[DEBUG] SOCKET_updateResource:\n\t' + params)
      // update_board from socket.io server
      commit('updateResource', params)
    },
    getBoard ({commit}) {
      // initially fetch Board from backend
      commit('changeLoadingState', true)
      // context.commit is the callback passed to client.getResources
      client.getResources(commit)
      commit('changeLoadingState', false)
    },
    getHistory ({commit}, name) {
      client.getHistory(name, commit)
    }
  }
})