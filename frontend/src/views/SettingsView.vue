<template>
  <v-app>
    <v-main>
      <v-container fluid fill-height>
        <v-row align="center" justify="center" class="fill-height">
          <v-col cols="12" sm="8" md="6">
            <v-card class="elevation-2">
              <v-toolbar color= 'gray'>
                <v-toolbar-title class="custom-toolbar-title">Settings</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text class="pa-10">
                <v-form>
                  <v-row>
                    <v-col cols="2" style="display: flex; align-items: center; justify-content: flex-end;">
                      <span>Username: </span>
                    </v-col>
                    <v-col>
                      <v-text-field 
                      type="text" 
                      hide-details>
                    </v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="2" style="display: flex; align-items: center; justify-content: flex-end;">
                      <span>Name: </span>
                    </v-col>
                    <v-col>
                      <v-text-field 
                      type="text" 
                      hide-details
                    ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row justify="center">
                    <v-col cols="auto" class="d-flex align-center">
                      <v-switch
                        label="Email Notifications"
                        color="primary"
                        true-icon="mdi-email"
                        false-icon="mdi-email-off"
                      ></v-switch>
                    </v-col>
                  </v-row>
                  <v-row class="justify-center pb-8">
                    <v-btn color = 'grey' class="white--text fixed-button" rounded>
                    Confirm 
                  </v-btn>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>


<script>
import { useTheme } from 'vuetify';

export default {
  name: "SettingsPage",
  data() {
    return {

    };
  },
  computed: {
  },
  watch: {
  },
  mounted() {
  }
};

</script>

<style scoped>

.custom-toolbar-title {
  color: #060000; /* Change this to your desired color */
}
</style>