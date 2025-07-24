<template>
  <div class='m-5'>
    <div class="flex items-baseline justify-between mb-4">
        <h2 class="text-gray-900 font-semibold">Links</h2>
        <Button variant="solid" @click="createDialogShown = true">Create</Button>
    </div>
    <ListView v-if="links.data"
    rowKey="name"
    :columns="[{
        label: 'Short Link',
        key: 'name',
        width: 0.4
    },
    {
        label: 'Destination',
        key: 'destination_url'
    },
    {
        label: 'Description',
        key: 'description'
    }]"
    :rows="links.data"
    :options="{
        shortToolTip: false,
        selectable: false
    }"
    />
    <Dialog :options="{
        title: 'Short Link',
        size: 'xl',
        actions: [{
            label: 'Create',
            variant: 'solid',
            onClick(close){
              links.insert.submit({
                ...newLink
              })
              close();
            }
        }]
        }" v-model="createDialogShown">
        <template #body-content>
          <form class="space-y-3">
              <FormControl
                  type="text"
                  label="Short"
                  v-model="newLink.short_link"
              />
              <FormControl
                  type="text"
                  label="destination_url"
                  v-model="newLink.destination_url"
              />
              <FormControl
                  type="textarea"
                  label="description"
                  v-model="newLink.description"
              />
          </form>
          <ErrorMessage class="mt-2" :message="links.insert.error"
          />
        </template>
        <template #actions>

        </template>
    </Dialog>
    
  </div>
</template>

<script setup>
import { ref } from "vue"
import { ListView, Dialog, FormControl, ErrorMessage } from "frappe-ui"
//import { createListResource } from 'frappe-ui'
import { useList } from "frappe-ui" //working 
import { reactive } from 'vue'
const createDialogShown = ref(false)
const newLink = reactive ({
    name:'',
    description: '',
    destination_url: ''
})
const links = useList({
  doctype: 'Short Link',
  fields: ['name','destination_url','description'],
  orderBy: 'creation desc' 
})
</script>


<!-- 
            <form>
                <FormControl
                    type="text"
                    label="Short"
                    v-model="newLink.name"
                />
            </form>

            const newLink = reactive ({
    name:'',
    description: '',
    destination_url: ''
}) -->