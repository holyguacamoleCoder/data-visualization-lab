<template>
  <div id="question-view" style="padding: 10px;">
    <div class="question" v-for="(question, index) in questions" :key="index">
      <h4>{{ question.name }}</h4>
      <div class="progress">
        <div class="progress-bar" :style="{ width: question.difficulty + '%' }">
          Difficulty: {{ question.difficulty }}
        </div>
      </div>
      <div class="progress">
        <div class="progress-bar" :style="{ width: question.score + '%' }">
          Score: {{ question.score }}
        </div>
      </div>
      <div>Avg Submit Num: {{ question.avgSubmitNum }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionView',
  data() {
    return {
      questions: [
        { name: 'Question 1', difficulty: 40, score: 80, avgSubmitNum: 5 },
        { name: 'Question 2', difficulty: 60, score: 70, avgSubmitNum: 3 },
        { name: 'Question 3', difficulty: 30, score: 90, avgSubmitNum: 7 }
      ]
    };
  }
};
</script>

<style scoped>
.question {
  margin-bottom: 20px;
}
.progress {
  background-color: #f5f5f5;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 10px;
}
.progress-bar {
  height: 20px;
  background-color: #3b82f6;
}
</style>
