<template>
  <v-container grid-list-md fluid>
    <v-layout
      row
      wrap
    >
      <!-- columns in different states --> 
      <v-flex v-for="(board, boardName) in this.loadedBoard" :key="boardName" xs12 sm6 md4 lg3>
        <span> {{ board.theme }} </span>
        <v-card color="blue-grey" dark>
            <v-card-title right>
              <v-icon middle>
              info
              </v-icon>
              <v-spacer></v-spacer>
              <span class="title font-weight-light mr-auto">&nbsp;{{ boardName }}</span>
            </v-card-title>
        </v-card>
        <v-divider inset></v-divider>

        <v-card :class="config_style[boardName]">
          <v-container fluid >
            <v-layout row wrap>
              <v-flex v-for="resource in board" :key="resource.name" align-center justify-center column>

                <v-card class="white lighten-4">
                  <v-card-title primary-title>
                    <div>
                      <div class="headline">{{ resource.name }}</div>
                      <span class="secondary--text font-weight-light">Since:</span>
                      <span class="primary--text ">
                        {{ resource.last_changed_at }}</span><br>
                      <span class="secondary--text font-weight-light"
                      v-show="resource.used_by !== ''"
                      >
                        Used by:
                      </span>
                      <span class="primary--text"
                      v-show="resource.used_by !== ''"
                      >
                        {{ resource.used_by }}</span>

                    </div>

                  </v-card-title>

                <v-card-actions>

                    <v-dialog v-model="resEditDialog" persistent max-width="600px">
                      <v-btn slot="activator" flat>Edit</v-btn>
                      <v-card>
                        <v-card-title>
                          <span class="headline secondary--text font-weight-light">Edit</span>
                          <v-spacer></v-spacer>
                          <span class="headline ">{{ resource.name }}</span>
                        </v-card-title>
                        <v-card-text>
                          <v-container grid-list-md>
                            <v-layout wrap>
                              <v-flex xs12>
                                <v-text-field
                                  v-model.trim="usedBy"
                                  label="Name of New User*"
                                  required
                                  hint="from now on"
                                  persistent-hint
                                  prepend-icon="face"
                                ></v-text-field>
                              </v-flex>
                              <v-flex xs12>
                                <v-select
                                  v-model="newState"
                                  :items="['ci', 'free', 'occupied', 'testing']"
                                  menu-props="auto"
                                  label="New State*"
                                  hide-details
                                  prepend-icon="info"
                                  single-line
                                  required
                                ></v-select>
                              </v-flex>
                            </v-layout>
                          </v-container>
                          <!-- notice here
                            <small>*indicates required field</small>
                          --> 
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="blue darken-1" flat @click="resEditDialog = false">Cancel</v-btn>
                          <v-btn
                            color="blue darken-1"
                            flat
                            :loading="loadingDialog"
                            @click="commitResEdit(resource.name)"
                          >
                            Commit
                          </v-btn>

                        </v-card-actions>
                      </v-card>
                    </v-dialog>

                  <v-btn flat class="accent--text ">History</v-btn>
                  <v-spacer></v-spacer>
                  <v-btn icon @click="resource.show = (resource.show === undefined) ? true : (!resource.show)">
                    <v-icon v-if="resource.show" >keyboard_arrow_down</v-icon>
                    <v-icon v-if="!resource.show" >keyboard_arrow_up</v-icon>
                  </v-btn>
                </v-card-actions>
                <v-slide-y-transition>
                  <v-card-text class="font-weight-light" v-show="resource.show">

                    <span class="secondary--text font-weight-light">Changed by:</span>
                    <span class="primary--text ">
                      {{ resource.last_changed_by }}</span><br>

                    <span class="secondary--text font-weight-light">Scale:</span>
                    <span class="primary--text ">
                      {{ resource.scale }}</span><br>

                  </v-card-text>
                </v-slide-y-transition>

                </v-card>

              </v-flex>

            </v-layout>
          </v-container>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
  import { mapGetters, mapActions, mapMutations } from 'vuex'

  export default {
    data: () => ({
      config_style: {
        'ci': 'accent',
        'free': 'success',
        'occupied': 'error',
        'testing': 'warning',
      },
      resEditDialog: false,
      loadingDialog: false,
      usedBy: '',
      newState: ''
    }),
    watch: {
      loadingDialog (val) {
        if (!val) return
        setTimeout(() => (this.loadingDialog = false), 4000)
        this.loadedBoard
      }
    },
    computed: {
      // `this.loadedBoard()` as `this.$store.getters('loadedBoard')`
      ...mapGetters([
        'loadedBoard',
        'getLoading'
      ]),
      ...mapMutations([
        'changeShowState',
        'changeLoadingState'
      ])
    },
    created () {
      // this.getBoard()
      this.$store.dispatch('getBoard')
    },
    methods: {
      commitResEdit: function (resName) {
        this.loadingDialog = true
        let params = {
          "name": resName,
          "used_by": this.usedBy,
          "state": this.newState
        }
        this.$socket.emit('up resource', params)
        this.changeLoadingState
      }
    }
  }
</script>

<style>

</style>
