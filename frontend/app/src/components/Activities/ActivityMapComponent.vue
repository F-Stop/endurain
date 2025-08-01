<template>
    <!-- map zone -->
    <div v-if="isLoading">
        <LoadingComponent />
    </div>
    <div v-else>
        <div v-if="hasGalleryItems">
            <div id="activityGallery" class="carousel slide position-relative">
                <div class="carousel-indicators position-absolute" style="z-index: 1030;">
                    <!-- Map indicator -->
                    <button v-if="activityStreamLatLng" type="button" data-bs-target="#activityGallery"
                        data-bs-slide-to="0" class="active" aria-current="true" aria-label="Map"></button>
                    <!-- Media indicators -->
                    <button v-for="(mediaItem, idx) in activityActivityMedia" :key="`indicator-${mediaItem.id || idx}`"
                        type="button" data-bs-target="#activityGallery"
                        :data-bs-slide-to="activityStreamLatLng ? idx + 1 : idx"
                        :class="{ active: !activityStreamLatLng && idx === 0 }"
                        :aria-current="!activityStreamLatLng && idx === 0 ? 'true' : 'false'"
                        :aria-label="`Media ${idx + 1}`"></button>
                </div>
                <div class="carousel-inner">
                    <!-- Map as first item -->
                    <div v-if="activityStreamLatLng" class="carousel-item active">
                        <div ref="activityMap" class="map rounded w-100" style="height: 300px;"
                            v-if="source === 'home'"></div>
                        <div ref="activityMap" class="map rounded w-100" style="height: 500px;"
                            v-if="source === 'activity'"></div>
                    </div>
                    <!-- Media items -->
                    <div v-for="(mediaItem, idx) in activityActivityMedia" :key="mediaItem.id || idx"
                        class="carousel-item position-relative" :class="{ active: !activityStreamLatLng && idx === 0 }"
                        :style="{ height: source === 'home' ? '300px' : '500px' }">
                        <img :src="`${endurainHost}${mediaItem.media_path.split('/').slice(4).join('/')}`"
                            class="d-block w-100 rounded" alt="Activity media"
                            :style="{ height: source === 'home' ? '300px' : '500px', objectFit: 'contain' }" />
                        <!-- Delete button for media -->
                        <button data-bs-toggle="modal" :data-bs-target="`#deleteMediaModal${mediaItem.id}`"
                            class="btn  position-absolute bottom-0 end-0 m-3" style="z-index: 1040;"
                            v-if="source === 'activity'">
                            <font-awesome-icon :icon="['fas', 'trash']" />
                        </button>

                        <!-- Modal for deleting gear from activity -->
                        <ModalComponent :modalId="`deleteMediaModal${mediaItem.id}`"
                            :title="t('activityMapComponent.modalMediaDeleteTitle')"
                            :body="`${t('activityMapComponent.modalMediaDeleteBody1')}${mediaItem.id}${t('activityMapComponent.modalMediaDeleteBody2')}${mediaItem.media_path.split('/').slice(-1).join('/')}?`"
                            actionButtonType="danger"
                            :actionButtonText="t('activityMapComponent.modalMediaDeleteTitle')"
                            :valueToEmit="mediaItem.id" :emitValue="true"
                            @submitAction="submitDeleteMediaFromActivity" />
                    </div>
                </div>
                <button class="carousel-control-prev position-absolute" type="button" data-bs-target="#activityGallery"
                    data-bs-slide="prev" style="z-index: 1030;">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next position-absolute" type="button" data-bs-target="#activityGallery"
                    data-bs-slide="next" style="z-index: 1030;">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>
        <div v-else-if="activityStreamLatLng && !hasGalleryItems">
            <div ref="activityMap" class="map rounded w-100" style="height: 300px;" v-if="source === 'home'"></div>
            <div ref="activityMap" class="map rounded w-100" style="height: 500px;" v-if="source === 'activity'"></div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch, onUnmounted } from 'vue';
import { useI18n } from "vue-i18n";
import { activityStreams } from '@/services/activityStreams';
import LoadingComponent from '@/components/GeneralComponents/LoadingComponent.vue';
import ModalComponent from '../Modals/ModalComponent.vue';
import L from 'leaflet';
import { useAuthStore } from "@/stores/authStore";
// Import Notivue push
import { push } from "notivue";
import { activityMedia } from '@/services/activityMediaService';

// Emit definition
const emit = defineEmits(['activityMediaDeleted']);

// Props declaration
const props = defineProps({
    activity: {
        type: Object,
        required: true,
    },
    activityActivityMedia: {
        type: Array,
        default: () => [],
    },
    source: {
        type: String,
        required: true,
    }
});

const { t } = useI18n();
const authStore = useAuthStore();
const isLoading = ref(true);
const activityStreamLatLng = ref(null);
const activityMap = ref(null);
const leafletMap = ref(null);
const hasGalleryItems = computed(() => {
    return Array.isArray(props.activityActivityMedia) && props.activityActivityMedia.length > 0;
});
const endurainHost = `${window.env.ENDURAIN_HOST}/`;

onMounted(async () => {
    try {
        if (authStore.isAuthenticated) {
            activityStreamLatLng.value = await activityStreams.getActivitySteamByStreamTypeByActivityId(props.activity.id, 7);
        } else {
            activityStreamLatLng.value = await activityStreams.getPublicActivitySteamByStreamTypeByActivityId(props.activity.id, 7);
        }
    } catch (error) {
        push.error(
            `${t("activityMapComponent.errorFetchingActivityStream")} - ${error}`,
        );
    } finally {
        isLoading.value = false;
        nextTick(() => {
            nextTick(() => {
                if (activityStreamLatLng.value) {
                    initMap();
                }
            });
        });
    }
});

onUnmounted(() => {
    if (leafletMap.value) {
        leafletMap.value.remove();
        leafletMap.value = null;
    }
});

const submitDeleteMediaFromActivity = async (mediaId) => {
    try {
        await activityMedia.deleteActivityMedia(mediaId)

        emit('activityMediaDeleted', mediaId);

        push.success(t("activityMapComponent.mediaDeletedSuccessfully"));
    } catch (error) {
        push.error(
            `${t("activityMapComponent.errorDeletingMedia")} - ${error}`,
        );
    }
};

const initMap = () => {
    if (!activityMap.value) return;

    const waypoints = activityStreamLatLng.value.stream_waypoints;
    const validWaypoints = waypoints.filter(waypoint => waypoint.lat && waypoint.lon);
    const latlngs = validWaypoints.map(waypoint => [waypoint.lat, waypoint.lon]);

    // Destroy previous map instance if exists
    if (leafletMap.value) {
        leafletMap.value.remove();
        leafletMap.value = null;
    }

    leafletMap.value = L.map(activityMap.value, {
        dragging: props.source === 'activity', // Enable if 'activity', disable if 'home'
        touchZoom: props.source === 'activity', // Enable if 'activity', disable if 'home'
        scrollWheelZoom: props.source === 'activity', // Enable if 'activity', disable if 'home'
        zoomControl: props.source === 'activity' // Enable if 'activity', disable if 'home'
    }).fitWorld();

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(leafletMap.value);

    L.polyline(latlngs, { color: 'blue' }).addTo(leafletMap.value);

    // Fit map to polyline bounds
    if (latlngs.length > 0) {
        leafletMap.value.fitBounds(latlngs);

        // Add start and end markers
        L.marker(latlngs[0], {
            icon: L.divIcon({ className: 'bg-success dot' })
        }).addTo(leafletMap.value);

        L.marker(latlngs[latlngs.length - 1], {
            icon: L.divIcon({ className: 'bg-danger dot' })
        }).addTo(leafletMap.value);
    }
};

watch(() => props.activityActivityMedia, async (newVal, oldVal) => {
    await nextTick(); // wait for DOM to update with the new v-if block
    if (activityStreamLatLng.value) {
        initMap();
    }
}, { deep: true });
</script>