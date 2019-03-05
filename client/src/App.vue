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
      >
        <span class="mr-2">Login</span>
      </v-btn>
    </v-toolbar>

    <v-content>
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </v-content>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  components: {
  },
  data () {
    return {
      //
    }
  }
}
</script>
