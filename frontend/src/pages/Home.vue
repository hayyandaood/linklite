<template>
  <div class="m-5 max-w-10xl"
>
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
          key: 'copy_to_clipboard'
        },
        {
          key: 'more_actions'
        }
      ]"
      :rows="links.list.data"
      :options="{
        shortToolTip: false,
        selectable: false,
        // onRowClick: (row) => {
        //     editDialogShown = true
        //     Object.assign(newLink, row)
        // },
        emptyState: {
          title: 'No records found',
          description: 'Create a new Link to get started',
          button: {
            label: 'New Link',
            variant: 'solid',
            onClick: () => {
              createDialogShown = true
            },
          },
        },
      }"
      >
      <template #cell="{ item, row, column }">
        <Button v-if="column.key === 'copy_to_clipboard'" class="cursor-printer" icon="copy" @click.stop="copyShortLinkToClipboard(row.short_link)" variant="outline" theme="blue" ></Button>
        <Dropdown
            v-else-if="column.key === 'more_actions'"
            :options="[
              {'label': 'Show Qr Code', onClick: () => {
                if (!row.rq_code) {
                  toast.warning('No QR Code Found for this Link')
                  return
                }
                qrCodeLink = row.qr_code;
                qrCodeshown =true;
              }}
            ]"
            >
            <Button icon="more-horizontal"></Button>
      </Dropdown>
        <span v-else class="font-medium text-ink-gray-7">
          {{ item }}
        </span>
      </template>
    </ListView>
    <Dialog
      :options="{
        title: 'New Short Link',
        size: 'xl',
        actions: [
          {
            label: 'Create',
            variant: 'solid',
            onClick: createShortLink,
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
            autofucos
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
    <Dialog v-model="qrCodeshown" 
      :options="{
        title: 'QR Code'
      }">
      <template #body-content>
        <div class="flex justify-center items-center">
          <img v-if="qrCodeLink" :src="qrCodeLink" alt="QR Code for Short Link"></img>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { onKeyStroke } from "@vueuse/core";
import { ListView, Dialog, FormControl, ErrorMessage, Dropdown } from "frappe-ui";
import { createListResource } from "frappe-ui";
import { reactive } from "vue";
import { toast } from 'vue-sonner'
import Button from "frappe-ui/src/components/Button/Button.vue";

const createDialogShown = ref(false);
const editDialogShown = ref(false);
const qrCodeshown = ref(false)
const qrCodeLink = null

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
  fields: ["short_link", "destination_url", "description","qr_code"],
  orderBy: "creation desc",
});

links.fetch();


function createShortLink(close) {
  links.insert.submit(
    {
      ...newLink,
    },
    {
      onSuccess() {
        newLink.short_link = "";
        newLink.description = "";
        newLink.destination_url = "";
        copyShortLinkToClipboard(newLink.short_link)
        close();
      },
    },
  );
}

function copyShortLinkToClipboard(text) {
  navigator.clipboard.writeText(`${window.location.origin}/${text}`);
  toast.success("Link copied to clipboard!")
}

</script>
