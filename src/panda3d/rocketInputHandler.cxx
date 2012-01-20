// Filename: rocketInputHandler.cxx
// Created by:  rdb (20Dec11)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

#include "rocketInputHandler.h"
#include "panda3d/buttonEventList.h"
#include "panda3d/dataGraphTraverser.h"
#include "panda3d/linmath_events.h"
#include "panda3d/keyboardButton.h"
#include "panda3d/mouseButton.h"

#include <Rocket/Core/Input.h>
#include <Rocket/Core/Context.h>

using namespace Rocket::Core::Input;

TypeHandle RocketInputHandler::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: RocketInputHandler::Constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
RocketInputHandler::RocketInputHandler(const string &name) : DataNode(name), _modifiers(0), _wheel_delta(0)
{
	_pixel_xy_input = define_input("pixel_xy", EventStoreVec2::get_class_type());
	_button_events_input = define_input("button_events", ButtonEventList::get_class_type());
} // end RocketInputHandler

////////////////////////////////////////////////////////////////////
//     Function: RocketInputHandler::Destructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
RocketInputHandler:: ~RocketInputHandler()
{
} // end ~RocketInputHandler

////////////////////////////////////////////////////////////////////
//     Function: RocketInputHandler::do_transmit_data
//       Access: Protected, Virtual
//  Description: The virtual implementation of transmit_data().  This
//               function receives an array of input parameters and
//               should generate an array of output parameters.  The
//               input parameters may be accessed with the index
//               numbers returned by the define_input() calls that
//               were made earlier (presumably in the constructor);
//               likewise, the output parameters should be set with
//               the index numbers returned by the define_output()
//               calls.
////////////////////////////////////////////////////////////////////
void RocketInputHandler::do_transmit_data(DataGraphTraverser *trav, const DataNodeTransmit &input, DataNodeTransmit &output)
{
	Thread *current_thread = trav->get_current_thread();
	MutexHolder holder(_lock);

	if (input.has_data(_pixel_xy_input))
	{
		// The mouse is within the window. Get the current mouse position.
		const EventStoreVec2 *pixel_xy;
		DCAST_INTO_V(pixel_xy, input.get_data(_pixel_xy_input).get_ptr());
		LVecBase2 p = pixel_xy->get_value();

		// Determine if mouse moved from last position
		if (p != _mouse_xy)
		{
			_mouse_xy_changed = true;
			_mouse_xy = p;
		} // end if
	} // end if

	ButtonEventList new_button_events;

	// Look for new button events.
	if (input.has_data(_button_events_input))
	{
		const ButtonEventList *this_button_events;
		DCAST_INTO_V(this_button_events, input.get_data(_button_events_input).get_ptr());
		int num_events = this_button_events->get_num_events();

		for (int i = 0; i < num_events; i++)
		{
			const ButtonEvent &be = this_button_events->get_event(i);

			switch (be._type)
			{
				case ButtonEvent::T_down:
				{
					if (be._button == KeyboardButton::control())
					{
						_modifiers |= KM_CTRL;
					}
					else if (be._button == KeyboardButton::shift())
					{
						_modifiers |= KM_SHIFT;
					}
					else if (be._button == KeyboardButton::alt())
					{
						_modifiers |= KM_ALT;
					}
					else if (be._button == KeyboardButton::meta())
					{
						_modifiers |= KM_META;

					}
					else if (be._button == MouseButton::wheel_up())
					{
						_wheel_delta -= 1;
					}
					else if (be._button == MouseButton::wheel_down())
					{
						_wheel_delta += 1;
					} // end if

					break;
				} // end case

				case ButtonEvent::T_repeat:
				{
					break;
				} // end case

				case ButtonEvent::T_up:
				{
					if (be._button == KeyboardButton::control())
					{
						_modifiers &= ~KM_CTRL;
					}
					else if (be._button == KeyboardButton::shift())
					{
						_modifiers &= ~KM_SHIFT;
					}
					else if (be._button == KeyboardButton::alt())
					{
						_modifiers &= ~KM_ALT;
					}
					else if (be._button == KeyboardButton::meta())
					{
						_modifiers &= ~KM_META;
					} // end if

					break;
				} // end case

				case ButtonEvent::T_keystroke:
				{
					_text_input.push_back(be._keycode);
					break;
				} // end case

				case ButtonEvent::T_resume_down:
				{
					break;
				} // end case

				case ButtonEvent::T_move:
				{
					break;
				} // end case

			} // end switch

			bool down = (be._type == ButtonEvent::T_down);

			if (down || be._type == ButtonEvent::T_up)
			{
				if (be._button == MouseButton::one())
				{
				  _mouse_buttons[1] = down;
				}
				else if (be._button == MouseButton::two()) {
				  _mouse_buttons[2] = down;
				}
				else if (be._button == MouseButton::three()) {
				  _mouse_buttons[3] = down;
				}
				else if (be._button == MouseButton::four()) {
				  _mouse_buttons[4] = down;
				}
				else if (be._button == MouseButton::five())
				{
				  _mouse_buttons[5] = down;
				}

				// In the order they are specified in Rocket/Core/Input.h

				else if (be._button == KeyboardButton::space())
				{
				  _keys[KI_SPACE] = down;
				}
				else if (be._button == KeyboardButton::backspace())
				{
				  _keys[KI_BACK] = down;
				}
				else if (be._button == KeyboardButton::tab())
				{
				  _keys[KI_TAB] = down;
				}
				else if (be._button == KeyboardButton::enter())
				{
				  _keys[KI_RETURN] = down;
				}
				else if (be._button == KeyboardButton::escape())
				{
				  _keys[KI_ESCAPE] = down;
				}
				else if (be._button == KeyboardButton::end())
				{
				  _keys[KI_END] = down;
				}
				else if (be._button == KeyboardButton::home())
				{
				  _keys[KI_HOME] = down;
				}
				else if (be._button == KeyboardButton::left())
				{
				  _keys[KI_LEFT] = down;
				}
				else if (be._button == KeyboardButton::up())
				{
				  _keys[KI_UP] = down;
				}
				else if (be._button == KeyboardButton::right())
				{
				  _keys[KI_RIGHT] = down;
				}
				else if (be._button == KeyboardButton::down())
				{
				  _keys[KI_DOWN] = down;
				}
				else if (be._button == KeyboardButton::insert())
				{
				  _keys[KI_INSERT] = down;
				}
				else if (be._button == KeyboardButton::del())
				{
					_keys[KI_DELETE] = down;
				}
				else if (be._button == KeyboardButton::caps_lock())
				{
					_keys[KI_CAPITAL] = down;
				}
				else if (be._button == KeyboardButton::f1())
				{
					_keys[KI_F1] = down;
				}
				else if (be._button == KeyboardButton::f10())
				{
					_keys[KI_F10] = down;
				}
				else if (be._button == KeyboardButton::f11())
				{
					_keys[KI_F11] = down;
				}
				else if (be._button == KeyboardButton::f12())
				{
					_keys[KI_F12] = down;
				}
				else if (be._button == KeyboardButton::f13())
				{
					_keys[KI_F13] = down;
				}
				else if (be._button == KeyboardButton::f14())
				{
					_keys[KI_F14] = down;
				}
				else if (be._button == KeyboardButton::f15())
				{
					_keys[KI_F15] = down;
				}
				else if (be._button == KeyboardButton::f16())
				{
					_keys[KI_F16] = down;
				}
				else if (be._button == KeyboardButton::f2())
				{
					_keys[KI_F2] = down;
				}
				else if (be._button == KeyboardButton::f3())
			   	{
					_keys[KI_F3] = down;
				}
				else if (be._button == KeyboardButton::f4())
				{
					_keys[KI_F4] = down;
				}
				else if (be._button == KeyboardButton::f5())
			   	{
					_keys[KI_F5] = down;
				}
				else if (be._button == KeyboardButton::f6())
				{
					_keys[KI_F6] = down;
				}
				else if (be._button == KeyboardButton::f7())
				{
					_keys[KI_F7] = down;
				}
				else if (be._button == KeyboardButton::f8())
				{
					_keys[KI_F8] = down;
				}
				else if (be._button == KeyboardButton::f9())
				{
					_keys[KI_F9] = down;
				}
				else if (be._button == KeyboardButton::help())
				{
					_keys[KI_HELP] = down;
				}
				else if (be._button == KeyboardButton::lalt())
				{
					_keys[KI_LMENU] = down;
				}
				else if (be._button == KeyboardButton::lcontrol())
				{
					_keys[KI_LCONTROL] = down;
				}
				else if (be._button == KeyboardButton::lshift())
				{
					_keys[KI_LSHIFT] = down;
				}
				else if (be._button == KeyboardButton::meta())
			   	{
					// Not sure which of these is correct...
					//_keys[KI_LWIN] = down;
					_keys[KI_LMETA] = down;
				}
				else if (be._button == KeyboardButton::num_lock())
			   	{
					_keys[KI_NUMLOCK] = down;
				}
				else if (be._button == KeyboardButton::page_down())
			   	{
					_keys[KI_NEXT] = down;
				}
				else if (be._button == KeyboardButton::page_up())
			   	{
					_keys[KI_PRIOR] = down;
				}
				else if (be._button == KeyboardButton::pause())
			   	{
					_keys[KI_PAUSE] = down;
				}
				else if (be._button == KeyboardButton::print_screen())
			   	{
					_keys[KI_SNAPSHOT] = down;
				}
				else if (be._button == KeyboardButton::ralt())
				{
					_keys[KI_RMENU] = down;
				}
				else if (be._button == KeyboardButton::rcontrol())
				{
					_keys[KI_RCONTROL] = down;
				}
				else if (be._button == KeyboardButton::rshift())
				{
					_keys[KI_RSHIFT] = down;
				}
				else if (be._button == KeyboardButton::scroll_lock())
				{
					_keys[KI_SCROLL] = down;
				/* What is shift_lock? It's not caps_lock apparently...

				}
				else if (be._button == KeyboardButton::shift_lock())
				{
					_keys[KI_SHIFT_LOCK] = down;
				*/
				}
				else
				{
					char asciiChar = be._button.get_ascii_equivalent();

					if ('0' <= asciiChar && asciiChar <= '9')
					{
						_keys[asciiChar - '0' + KI_0] = down;
					}
					else if ('a' <= asciiChar && asciiChar <= 'z')
					{
						_keys[asciiChar - 'a' + KI_A] = down;
					} // end if
				} // end if
			} // end if
		} // end for
	} // end if
} // end do_transmit_data

////////////////////////////////////////////////////////////////////
//     Function: RocketInputHandler::update_context
//       Access: Public
//  Description: Updates the libRocket context with the changes
//               that we have gathered in do_transmit_data.
//               Also calls Update() on the context.
////////////////////////////////////////////////////////////////////
void RocketInputHandler::update_context(Rocket::Core::Context *context, int xoffs, int yoffs)
{
	MutexHolder holder(_lock);

	if (_mouse_xy_changed)
	{
		_mouse_xy_changed = false;

		context->ProcessMouseMove(_mouse_xy.get_x() - xoffs, _mouse_xy.get_y() - yoffs, _modifiers);
	} // end if

	//printf("   MouseButtons...\n");
	//fflush(stdout);

	if (_mouse_buttons.size() > 0)
	{
		ButtonActivityMap::const_iterator it;
		for (it = _mouse_buttons.begin(); it != _mouse_buttons.end(); ++it)
		{
			// it->second is a boolean; so this is 'if button is pressed...'
			if (it->second)
			{
				context->ProcessMouseButtonDown(it->first - 1, _modifiers);
			}
			else
			{
				context->ProcessMouseButtonUp(it->first - 1, _modifiers);
			} // end if
		} // end for

		_mouse_buttons.clear();
	} // end if

	if (_wheel_delta != 0)
	{
		context->ProcessMouseWheel(_wheel_delta, _modifiers);
		_wheel_delta = 0;
	} // end if

	if (_keys.size() > 0)
	{
		ButtonActivityMap::const_iterator it;

		for (it = _keys.begin(); it != _keys.end(); ++it)
		{
			if (it->second)
			{
				context->ProcessKeyDown((KeyIdentifier) it->first, _modifiers);
			}
			else
			{
				context->ProcessKeyUp((KeyIdentifier) it->first, _modifiers);
			} // end if
		} // end for

		_keys.clear();
	} // end if

	if (_text_input.size() > 0)
	{
		pvector<short>::const_iterator it;
		for (it = _text_input.begin(); it != _text_input.end(); ++it)
		{
			fprintf(stdout, "Sending text %d.\n", *it);
			context->ProcessTextInput(*it);
		} // end for

		_text_input.clear();
	} // end if

	// Removed; this will be called explicitly outside of the input handler.
	//context->Update();
} // end update_context
