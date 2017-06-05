<?php
	function osCommandOverride($input){
		$input = escapeshellarg($input);
		return $input;
	}
?>