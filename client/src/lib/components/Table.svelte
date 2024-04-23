<script lang="ts">
	export let data: any;
</script>

<div class="overflow-x-auto">
	<table class="table">
		<!-- head -->
		<tbody>
			<!-- row 1 -->
			<tr>
				<td>Status</td>
				<td>{data.status || 'loading...'}</td>
			</tr>
			<!-- row 2 -->
			<tr>
				<td>Cat Weight</td>
				<td>{data.catWeight || 'fetching weight...'}</td>
			</tr>
			<!-- row 3 -->
			<tr>
				<td>Litter Level</td>
				<td>{data.litterLevel || 'calculating litter level...'}</td>
			</tr>

			<!-- row 3 -->
			<tr>
				<td>Weight Sensor</td>
				<td>{data.weightSensor || 'checking weight sensor...'}</td>
			</tr>
		</tbody>
	</table>
</div>
