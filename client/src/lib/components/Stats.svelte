<script lang="ts">
	import { fade, slide } from 'svelte/transition';
	import Icon from '@iconify/svelte';
	export let data = {
		status: 'loading...',
		catWeight: 'fetching weight...',
		litterLevel: 'calculating litter level...',
		weightSensor: 'checking weight sensor...'
	};
</script>

<div class="stats md:stats-vertical h-full w-full shadow">
	<div class="stat">
		<div class="stat-figure text-primary">
			<Icon icon="material-symbols:info" class="h-10 w-10" />
		</div>
		<div class="stat-title">Status</div>
		{#if data.status}
			<div class="stat-value text-2xl">{data.status}</div>
		{:else}
			<div class="stat-value text-2xl">loading...</div>
		{/if}
		<!-- <div class="stat-desc">Jan 1st - Feb 1st</div> -->
	</div>

	<div class="stat">
		<div class="stat-figure text-primary">
			<Icon icon="ion:levels" class="h-10 w-10" />
		</div>
		<!-- <div class="stat-desc">↗︎ 400 (22%)</div> -->

		<div class="stat-title">Litter Level</div>
		{#if data.status}
			<div class="stat-value text-2xl">
				{data.litterLevel}
			</div>
		{:else}
			<div class="stat-value text-2xl">loading...</div>
		{/if}
	</div>

	<div class="stat">
		<div class="stat-figure text-primary">
			<Icon icon="material-symbols:scale" class="h-10 w-10" />
		</div>
		<!-- <div class="stat-desc">↘︎ 90 (14%)</div> -->

		<div class="stat-title">Weight Sensor</div>
		{#if data.status}
			<div class="stat-value text-2xl">
				{data.weightSensor}
			</div>
		{:else}
			<div class="stat-value text-2xl">loading...</div>
		{/if}
	</div>

	<div class="stat">
		<div class="stat-figure text-primary">
			<Icon icon="streamline-nature-ecology-cat-head-cat-pet-animals-felyne" class="h-10 w-10" />
		</div>
		<!-- <div class="stat-desc">↘︎ 90 (14%)</div> -->

		<div class="stat-title">Cat Weight</div>
		{#if data.status}
			<div class="stat-value text-2xl">
				{data.catWeight + ' lbs'}
			</div>
		{:else}
			<div class="stat-value text-2xl">loading...</div>
		{/if}
	</div>
</div>
