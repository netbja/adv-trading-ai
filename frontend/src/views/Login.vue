<template>
  <div class="login-container">
    <div class="login-card">
      <h1>🧠 Trading AI Pro</h1>
      <p>Connexion au Dashboard</p>
      
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Utilisateur</label>
          <input 
            type="text" 
            id="username" 
            v-model="username"
            placeholder="admin"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input 
            type="password" 
            id="password" 
            v-model="password"
            placeholder="••••••••"
            required
          >
        </div>
        
        <button type="submit" class="btn-login">
          Se connecter
        </button>
      </form>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

const login = () => {
  if (username.value === 'admin' && password.value === 'admin') {
    router.push('/')
  } else {
    error.value = 'Identifiants incorrects'
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

p {
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ecf0f1;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #3498db;
}

.btn-login {
  width: 100%;
  padding: 0.75rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-login:hover {
  background: #2980b9;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #e74c3c;
  color: white;
  border-radius: 8px;
}
</style> 