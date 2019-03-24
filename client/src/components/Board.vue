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

                      <span class="accent--text">
                        {{ resource.last_changed_at | timeFormat }}</span><br>
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

                      <v-dialog v-model="resource.edit_dialog" persistent max-width="600px">
                        <v-btn slot="activator" flat v-if="!resource.show_details">Edit</v-btn>
                        <v-card >
                          <v-card-title>
                            <span class="headline secondary--text font-weight-light" v-if="loginInfo.loggedIn">Edit</span>
                            <span class="headline secondary--text font-weight-light" v-if="!loginInfo.loggedIn">Please login to edit</span>
                            <v-spacer></v-spacer>
                            <span class="headline ">{{ resource.name }}</span>
                          </v-card-title>
                          <v-card-text>
                            <v-form v-model="valid">
                              <v-container grid-list-md>
                                <v-layout wrap>
                                  <v-flex xs12>
                                    <v-text-field
                                      v-model.trim="usedBy"
                                      label="Name of New User*"
                                      required
                                      :rules="nameRules"
                                      hint="Name who will occupy it from now on."
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
                                      :rules="stateRules"
                                      ba-2
                                    ></v-select>
                                  </v-flex>
                                  <v-flex xs12>
                                    <v-textarea
                                      v-model="note"
                                      prepend-icon="note"
                                      hint="leave a note to the team"
                                    ></v-textarea>
                                  </v-flex>

                                </v-layout>
                              </v-container>
                            <!-- notice here
                              <small>*indicates required field</small>
                            --> 
                            </v-form>
                          </v-card-text>
                          <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" flat @click="resource.edit_dialog = false">Cancel</v-btn>
                            <v-btn
                              color="blue darken-1"
                              flat
                              :loading="loadingDialog"
                              @click="commitResEdit(resource.name)"
                              :disabled="valid === false || !loginInfo.loggedIn"
                            >
                              Commit
                            </v-btn>

                          </v-card-actions>
                        </v-card>
                      </v-dialog>

                    <v-btn
                      flat
                      :class="config_style[boardName]+'--text text--lighten-1'"
                      :to="'/resource/' + resource.name +'/history'"
                      v-if="!resource.show_details"
                    >
                      History
                    </v-btn>

                    <v-spacer></v-spacer>
                    <v-btn icon @click="resource.show_details = !resource.show_details">
                      <v-icon v-if="resource.show_details" >keyboard_arrow_down</v-icon>
                      <v-icon v-if="!resource.show_details" >keyboard_arrow_up</v-icon>
                    </v-btn>
                  </v-card-actions>
                  <v-slide-y-transition>
                      <v-card-text class="font-weight-light" v-show="resource.show_details">
                        <v-layout wrap>
                          <v-flex xs12 ba-1>
                            <span class="secondary--text font-weight-light">Changed by:</span>
                            <span class="primary--text ">
                              {{ resource.last_changed_by }}</span><br>

                            <span v-if="resource.note" class="secondary--text font-weight-light">Note:</span><br>
                            <span v-if="resource.note" class="font-weight-thin">
                              {{ resource.note }}
                            </span>
                          </v-flex>

                          <v-flex xs12 pa-1>
                            <v-chip color="purple lighten-1" text-color="white" class="font-weight-light" small >{{ resource['hardware_type'] }}</v-chip>
                            <v-chip color="primary" text-color="white" class="font-weight-light" small >
                              {{ resource['scale'] }} Servers
                              <v-icon right small>dns</v-icon>
                            </v-chip>
                          </v-flex>
                        </v-layout>
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
  import { mapState, mapGetters, mapMutations } from 'vuex'

  export default {
    data: () => ({
      config_style: {
        'ci': 'accent',
        'free': 'success',
        'occupied': 'error',
        'testing': 'warning',
      },
      loadingDialog: false,
      valid: false,
      usedBy: '',
      newState: '',
      note: '',
      nameRules: [
        v => !!v || 'Newly used-by name is required',
        v => v.length <= 25 || 'Name must be less than 25 characters'
      ],
      stateRules: [
        v => !!v || 'New state is required',
      ]
    }),
    watch: {
      loadingDialog (val) {
        if (!val) return
        setTimeout(() => (this.loadingDialog = false), 4000)
      },
    },
    computed: {
      // `this.loadedBoard()` as `this.$store.getters('loadedBoard')`
      ...mapState([
        'loginInfo',
      ]),
      ...mapGetters([
        'loadedBoard',
        'getLoading'
      ]),
      ...mapMutations([
        'changeShowState',
        'changeDialogState',
      ]),
    },
    created () {
      // cannot use mappAction this.getBoard() here
      this.$store.dispatch('getBoard')
    },
    methods: {
      commitResEdit: function (resName) {
        this.loadingDialog = true
        let params = {
          "name": resName,
          "used_by": this.usedBy,
          "state_name": this.newState,
          "note": this.note,
        }
        this.$socket.emit('update resource', params)
      }
    }
  }
</script>

<style>

</style>
