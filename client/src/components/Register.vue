<template>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md5>
            <v-card class="elevation-1">
              <v-toolbar dark color="teal lighten-1">
                <v-toolbar-title>Register</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-icon large>face</v-icon>
              </v-toolbar>
              <v-card-text>
                <v-form v-model="valid">
                  <v-text-field :rules="rules" prepend-icon="person" name="login" label="Username" v-model.trim="username" type="text"></v-text-field>
                  <v-text-field :rules="rules" prepend-icon="lock" name="password" label="New password" v-model="passwd" type="password"></v-text-field>

                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn dark
                  color="teal"
                  :loading="loadingDialog"
                  @click="clickRegister()"
                  to="/"
                  :disabled="valid === false"
                  >Register</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    data: () => ({
      username: '',
      passwd:'',
      loadingDialog: false,
      valid: false,
      rules: [
        v => !!v || 'field is required',
      ],
    }),
    watch: {
      loadingDialog (val) {
        if (!val) return
        setTimeout(() => (this.loadingDialog = false), 4000)
      },
      '$route' (from, to) {
        this.$store.dispatch('getHistory', this.$route.params.name)
      }
    },
    methods: {
      clickRegister: function () {
        this.loadingDialog = true
        let registerData = {
          "passwd": this.passwd,
          "username": this.username,
        }
        this.$socket.emit('register user', registerData)
      }
    }
  }
</script>

<style>

</style>
