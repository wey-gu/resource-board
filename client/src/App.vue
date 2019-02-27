<template>
  <v-app>
    <v-toolbar app color="BLACK" dark>
      <v-toolbar-title class="headline text-uppercase">
        <span class="font-weight-light">Resourse</span>
        <span>Board</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        flat
      >
        <span class="mr-2">Login</span>
      </v-btn>
    </v-toolbar>

    <v-content>
      <Board/>
    </v-content>
  </v-app>
</template>

<script>
import Board from './components/Board'

export default {
  name: 'App',
  components: {
    Board
  },
  data () {
    return {
      //
    }
  }
}
</script>
