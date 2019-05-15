////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Octolapse - A plugin for OctoPrint used for making stabilized timelapse videos.
// Copyright(C) 2019  Brad Hochgesang
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// This program is free software : you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.If not, see the following :
// https ://github.com/FormerLurker/Octolapse/blob/master/LICENSE
//
// You can contact the author either through the git - hub repository, or at the
// following email address : FormerLurker@pm.me
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include "stabilization_results.h"

stabilization_results::stabilization_results()
{
	bool success = false;
	double seconds_elapsed = 0;
	long gcodes_processed = 0;
	long lines_processed = 0;
}
stabilization_results::~stabilization_results()
{	
	while (!snapshot_plans_.empty()) {
		snapshot_plan* p = snapshot_plans_.back();
		snapshot_plans_.pop_back();
		delete p;
	}
	

		/*for (unsigned int index = 0; index < (*p_snapshot_plans).size(); index++)
		{
			delete (*p_snapshot_plans)[index];
			(*p_snapshot_plans)[index] = NULL;
		}
		p_snapshot_plans->clear();
		delete p_snapshot_plans;
		p_snapshot_plans = NULL;*/
	
}