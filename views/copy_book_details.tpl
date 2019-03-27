<div class="copy_info">
    <p>
    % if copy_availability_details['num_copies'] == 1:
        {{copy_availability_details['num_copies']}} copy, {{copy_availability_details['num_available']}} currently available.
    % else:
        {{copy_availability_details['num_copies']}} copies, {{copy_availability_details['num_available']}} currently available. 
    % end
    % if copy_availability_details['num_available'] == 0:   
        Next due back: {{copy_availability_details['next_due']}}
    % end
    </p>
</div>