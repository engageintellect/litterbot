<script>
	import '../app.pcss';
	import Nav from '$lib/components/Nav.svelte';
</script>

<div>
	<Nav />

	<div>
		<slot />
	</div>
</div>
