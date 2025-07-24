<template>
  <div class='m-5'>
    <div class="flex items-baseline justify-between mb-4">
        <h2 class="text-gray-900 font-semibold">Links</h2>
        <Button variant="solid" @click="createDialogShown = true">
			Create Link
			<template #suffix>
				<span class=" font-mono bg-white/80 text-gray-700 rounded-sm px-1">C</span>            
            </template>
		</Button>
    </div>
    <ListView v-if="links.data"
    rowKey="name"
    :columns="[{
        label: 'Short Link',
        key: 'short_link',
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
            async onClick(close) {
                console.log('About to submit:', { ...newLink })
                await links.insert.submit({ ...newLink })
                console.log('Success! Closing dialog.')
                // Reset form
                newLink.short_link = ''
                newLink.description = ''
                newLink.destination_url = ''
                // Reload the list to show new data
                links.reload()
                close()
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
                  label="Destination URL"
                  v-model="newLink.destination_url"
              />
              <FormControl
                  type="textarea"
                  label="Description"
                  v-model="newLink.description"
              />
          </form>
          <ErrorMessage class="mt-2" :message="links.insert.error" />
        </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue"
import { onKeyStroke } from "@vueuse/core";
import { ListView, Dialog, FormControl, ErrorMessage, Button } from "frappe-ui"
import { useList } from "frappe-ui"

const createDialogShown = ref(false)

const newLink = reactive({
    short_link: '',
    description: '',
    destination_url: '',
})

onKeyStroke(["c", "C"], () => {
	createDialogShown.value = true;
});
const links = useList({
  doctype: 'Short Link',
  fields: ['short_link','destination_url','description'],
  orderBy: 'creation desc' 
})
</script>