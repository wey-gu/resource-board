<template>
  <v-app>
    <v-toolbar app color="BLACK" dark>
      <div>
      <v-btn flat color="WHITE" to="/" class="shadow-none">
        <v-toolbar-title class="headline text-uppercase">
          <span class="font-weight-light">
            resourse</span><span>board
          </span>
        </v-toolbar-title>
      </v-btn>
      </div>
      <v-spacer></v-spacer>

      <v-btn
        flat
        to="/"
        @click="logout()"
        v-if="this.loginInfo.loggedIn === true"
      >
        <span class="mr-2">Logout</span>
      </v-btn>

      <v-btn
        flat
        to="/login"
        v-if="this.loginInfo.loggedIn !== true"
      >
        <span class="mr-2">Login</span>
      </v-btn>
      <v-btn
        flat
        to="/register"
        v-if="this.loginInfo.loggedIn !== true"
      >
        <span class="mr-2">Register</span>
      </v-btn>
    </v-toolbar>

    <v-content>
      <div>
        <v-alert
          :value="this.alertVisiable"
          dismissible
          :type="this.getAlert.type"
          icon="info"
        >
          {{ this.getAlert.msg }}
        </v-alert>
      </div>

      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </v-content>
  </v-app>
</template>

<script>
  import { mapState, mapGetters, mapMutations } from 'vuex'

  export default {
    name: 'App',
    components: {
    },
    data () {
      return {
      }
    },
    computed: {
      // `this.loadedBoard()` as `this.$store.getters('loadedBoard')`
      ...mapState([
        'loginInfo',
      ]),
      ...mapGetters([
        'getAlert',
        'alertVisiable',
      ]),
      ...mapMutations([
        'alerting',
      ])
    },
    methods: {
      logout: function () {
        this.$socket.emit('logout user')
      }
    }
  }
</script>
