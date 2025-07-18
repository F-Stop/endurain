<template>
    <div class="col">
		<div class="bg-body-tertiary rounded p-3 shadow-sm">
			<!-- list zone -->
			<ul class="list-group list-group-flush">
				<!-- import zone -->
				<!-- bulk import zone -->
				<li class="list-group-item d-flex justify-content-between bg-body-tertiary px-0">
					<div class="d-flex align-items-center">
						<font-awesome-icon :icon="['fas', 'file-import']" size="2x" />
						<div class="ms-3">
							<div class="fw-bold">
								{{ $t("settingsImportZone.bulkImportIntegrationTitle") }}
							</div>
							{{ $t("settingsImportZone.bulkImportIntegrationBody") }}
						</div>
					</div>
					<div class="d-flex align-items-center">
						<!-- import button -->
						<a href="#" class="btn btn-primary" role="button" @click="submitBulkImport">{{ $t("settingsImportZone.buttonBulkImport") }}</a>
					</div>
				</li>
				<!-- Strava bulk-export import zone -->
				<li class="list-group-item d-flex justify-content-between bg-body-tertiary px-0">
					<div class="d-flex align-items-center">
						<font-awesome-icon :icon="['fas', 'file-import']" size="2x" />
						<div class="ms-3">
							<div class="fw-bold">
								{{ $t("settingsImportZone.stravaImportIntegrationTitle") }}
							</div>
							{{ $t("settingsImportZone.stravaImportIntegrationBody") }}
						</div>
					</div>
					<div class="d-flex align-items-center">
						<!-- import button -->
						<a href="#" class="btn btn-primary" role="button" @click="submitStravaBikeGearImport">{{ $t("settingsImportZone.stravaImportbuttonBikeGear") }}</a>
					</div>
				</li>
			</ul>

		</div>
	</div>
</template>

<script>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
// Import Notivue push
import { push } from "notivue";
// Importing the stores
import { useAuthStore } from "@/stores/authStore";
// Importing the services
//import { strava } from "@/services/stravaService";
import { activities } from "@/services/activitiesService";
//import { garminConnect } from "@/services/garminConnectService";
// Import the components
import ModalComponent from "@/components/Modals/ModalComponent.vue";
import ModalComponentNumberAndStringInput from "@/components/Modals/ModalComponentNumberAndStringInput.vue";
import ModalComponentNumberInput from "@/components/Modals/ModalComponentNumberInput.vue";
import ModalComponentDateRangeInput from "@/components/Modals/ModalComponentDateRangeInput.vue";
//import GarminConnectLoginModalComponent from "./SettingsIntegrations/GarminConnectLoginModalComponent.vue";

export default {
	components: {
		ModalComponent,
		ModalComponentNumberAndStringInput,
		ModalComponentNumberInput,
		ModalComponentDateRangeInput,
		//GarminConnectLoginModalComponent,
	},
	setup() {
		const authStore = useAuthStore();
		const { locale, t } = useI18n();

		async function submitBulkImport() {
			try {
				await activities.bulkImportActivities();

				// Show the loading alert.
				push.info(t("settingsIntegrationsZone.loadingMessageBulkImport"));
			} catch (error) {
				// If there is an error, show the error alert.
				push.error(
					`${t("settingsIntegrationsZone.errorMessageUnableToImportActivities")} - ${error}`,
				);
			}
		}

		async function submitStravaBikeGearImport() {
			try {
				await activities.stravaBikeGearImportActivities();

				// Show the loading alert.
				push.info(t("settingsIntegrationsZone.loadingMessageStravaBikeGearImport"));
			} catch (error) {
				// If there is an error, show the error alert.
				push.error(
					`${t("settingsIntegrationsZone.errorMessageUnableToImportBikeGear")} - ${error}`,
				);
			}
		}


		return {
			authStore,
			t,
			submitBulkImport,
			submitStravaBikeGearImport,
		};
	},
};
</script>
