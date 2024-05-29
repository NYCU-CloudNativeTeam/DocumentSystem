<template>
  <v-container>
    <v-row>
      <v-col lg="6">
        <h2 class="intro-text">Welcome to the Document Center</h2>
        <!-- <p class="description">Hi</p> -->
        <v-btn color = "indigo" class="white--text fixed-button" rounded >
          Get Started 
          <v-icon right>mdi-arrow-right</v-icon>
        </v-btn>
      </v-col>
      <v-col lg="6">
        <v-img src="/discussion.png"></v-img>
      </v-col>
      </v-row>
  </v-container>
</template>

<style scoped>
 h2.intro-text {
   font-size: 4rem;
   font-weight: 700;
   margin-bottom: 1rem;
   
 }
 .v-col {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.fixed-button {
  width: 170px;
  height: 50px;
}
</style>
