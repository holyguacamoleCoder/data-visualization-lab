<template>
  <div id="student-view" style="height: 400px;">
    <ul v-show="submissions.length > 0">
      <li v-for="submission in submissions" :key="submission.index">
        {{ JSON.stringify(submission) }}
        6666
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentView',
  data() {
    return {
      submissions: [],
      treeData: []
    }
  },
  mounted() {
    this.fetchSubmissions()
    this.fetchTreeData()
  },
  methods: {
    async fetchSubmissions() {
      try {
        const response = await axios.get('http://localhost:5000/api/submissions', {
          params: {
            limit: 10,
          }
        });
        this.submissions = response.data;
        console.log('Submissions:', this.submissions);
      } catch (error) {
        console.error('Failed to fetch submissions:', error);
      }
    },
    async fetchTreeData() {
      try {
        const response = await axios.get('http://localhost:5000/api/tree_data', {
          params: {
            limit: 10,
          }
        });
        this.treeData = response.data;
        console.log('TreeData:', this.treeData);
      } catch (error) {
        console.error('Failed to fetch submissions:', error);
      }
    },
  }
};
</script>

<style scoped lang="less">
#student-view {
  width: 100%;
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    margin: 0.5em 0;
  }
}
</style>
