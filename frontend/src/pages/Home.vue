<template>
  <div class="m-5">
    <div class="flex items-baseline justify-between mb-4">
      <h2 class="text-gray-900 font-semibold">Links</h2>
      <Button variant="solid" @click="createDialogShown = true">
        Create Link
        <template #suffix>
          <span class="font-mono bg-white/80 text-gray-700 rounded-sm px-1"
            >C</span
          >
        </template>
      </Button>
    </div>
    <ListView
      v-if="links.list.data"
      rowKey="name"
      :columns="[
        {
          label: 'Short Link',
          key: 'short_link',
          width: 0.4,
        },
        {
          label: 'Destination',
          key: 'destination_url',
        },
        {
          label: 'Description',
          key: 'description',
        },
      ]"
      :rows="links.list.data"
      :options="{
        shortToolTip: false,
        selectable: false,
        onRowClick: (row) => {
            editDialogShown = true
            Object.assign(newLink, row)
        }
      }"
    />
    <Dialog
      :options="{
        title: 'New Short Link',
        size: 'xl',

        actions: [
          {
            label: 'Create',
            variant: 'solid',
            onClick(close) {
              links.insert.submit(
                {
                  ...newLink,
                },
                {
                  onSuccess() {
                    newLink.short_link = '';
                    newLink.destination_url = '';
                    newLink.description = '';
                    close();
                  },
                }
              );
            },
          },
        ],
      }"
      v-model="createDialogShown"
    >
      <template #body-content>
        <form class="space-y-3">
          <FormControl
            type="text"
            label="Destination URL"
            placeholder="https://youtube.com/@buildwithhussain"
            v-model="newLink.destination_url"
            autofocus
          />

          <FormControl
            type="text"
            placeholder="bwh"
            label="Short Link"
            v-model="newLink.short_link"
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
    <Dialog
      :options="{
        title: 'Edit Link',
        size: 'xl',

        actions: [
          {
            label: 'Save',
            variant: 'solid',
            onClick (close) {
              links.setValue.submit(
                {
                  name: newLink.short_link,
                  description: newLink.description,
                  destination_url: newLink.destination_url
                },
                {
                  onSuccess() {
                    newLink.short_link = '';
                    newLink.destination_url = '';
                    newLink.description = '';
                    links.fetch();
                    close();
                  },
                }
              );
            },
          },
          {
            label: 'Delete',
            variant: 'outline',
            theme: 'red',
            onClick(close){
                links.delete.submit(newLink.short_link, {
                    onSuccess() {
                        close();
                    }
                })
            }
          }
        ],
      }"
      v-model="editDialogShown"
    >
      <template #body-content>
        <form class="space-y-3">
          <FormControl
            type="text"
            label="Destination URL"
            placeholder="https://youtube.com/@buildwithhussain"
            v-model="newLink.destination_url"
            autofocus
          />

          <FormControl
            type="text"
            placeholder="bwh"
            label="Short Link"
            v-model="newLink.short_link"
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
import { ref, reactive } from "vue";
import { onKeyStroke } from "@vueuse/core";
import { ListView, Dialog, FormControl, ErrorMessage, Button } from "frappe-ui";
//import { useList } from "frappe-ui";
import { createListResource } from "frappe-ui";

const createDialogShown = ref(false);
const editDialogShown = ref(false);

const newLink = reactive({
  short_link: "",
  description: "",
  destination_url: "",
});

onKeyStroke(["c", "C"], () => {
  createDialogShown.value = true;
});
const links = createListResource({
  doctype: "Short Link",
  fields: ["short_link", "destination_url", "description"],
  orderBy: "creation desc",
});

links.fetch();
</script>
