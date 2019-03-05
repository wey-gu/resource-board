<template>
  <v-container>
    <v-flex xs-8>
      <v-container>
        <v-flex md-12 >
          <span class="title font-weight-light">Historical changes of </span>
          <span class="title font-weight-regular">{{ this.resourceName }}</span>
        </v-flex>
      </v-container>
    </v-flex>
    <v-container v-if="this.noHistoryError" >

      <v-dialog
        v-model="this.noHistoryError"
        width="600"
      >
        <v-card>
          <v-card-title
            class="headline grey lighten-2"
            primary-title
          >
            404
          </v-card-title>

          <v-card-text>
            <v-icon x-large color="error">
            cancel
            </v-icon>
            <span
              class="font-weight-thin display-1">
              OPPS... no history for {{ this.resourceName }} now.
            </span>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              flat
              to="/"
            >
              <v-icon color="primary">
                home
              </v-icon>

            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </v-container>

    <v-timeline v-if="!this.noHistoryError">
      <v-timeline-item
        :color="config_style[record['state']] + ' lighten-1'"
        fill-dot
        v-for="record in this.history" :key="record['last_changed_at']"
      >
        <v-card>
          <v-card-title :class="config_style[record['state']] + ' lighten-1'">
            <h2 class="subheading white--text font-weight-light">{{ record['last_changed_at'] | timeFormatFull }}</h2>
          </v-card-title>
          <v-container>
            <v-layout wrap column>
              <v-flex xs8 pb-2>
                <v-chip color="purple lighten-1" text-color="white">{{ record['state'] }}</v-chip>
                  <v-chip v-if="record['used_by'] !== ''" >
                  <v-avatar class="teal lighten-2">by</v-avatar>
                  {{ record['used_by'] }}
                </v-chip>
              </v-flex>

              <v-divider v-if="record['note'] !== '' " ></v-divider>
              <v-flex xs10 pa-2 v-if="record['note'] !== ''" class="grey--text font-weight-light">
                {{ record['note'] }}
              </v-flex>

            </v-layout>
          </v-container>
        </v-card>
      </v-timeline-item>
    </v-timeline>
  </v-container>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    data: () => ({
      config_style: {
        'ci': 'accent',
        'free': 'success',
        'occupied': 'error',
        'testing': 'warning',
      }
    }),
    watch: {
      '$route' (from, to) {
        this.$store.dispatch('getHistory', this.$route.params.name)
      }
    },
    computed: {
      // `this.loadedBoard()` as `this.$store.getters('loadedBoard')`
      ...mapGetters([
        'getHistoryByName'
      ]),
      resourceName: function () {
        return this.$route.params.name
      },
      history: function () {
        return this.getHistoryByName(this.resourceName)
      },
      noHistoryError: function () {
        return ((this.history === undefined) || (this.history.length === 0) && this.$route.path.includes('history'))
      }
    },
    created () {
      // this.getBoard()
      this.$store.dispatch('getHistory', this.$route.params.name)
    }
  }
</script>

<style>

</style>
